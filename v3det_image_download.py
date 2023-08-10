import io
import argparse
import concurrent.futures
import json
import os
import time
import urllib.error
import urllib.request

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--output_folder", type=str, default="V3Det")
parser.add_argument("--max_retries", type=int, default=3)
parser.add_argument("--max_workers", type=int, default=16)
args = parser.parse_args()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}


def cache(response):
    f = io.BytesIO()
    block_sz = 8192
    while True:
        buffer = response.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    return f

def download_image(url, path, timeout):
    result = {
        "status": "",
        "url": url,
        "path": path,
    }
    cnt = 0
    while True:
        try:
            response = urllib.request.urlopen(urllib.request.Request(url=url, headers=headers), timeout=timeout)
            image_path = os.path.join(args.output_folder, path)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            f = cache(response)
            with open(image_path, "wb") as fp:
                fp.write(f.getvalue())
            result["status"] = "success"
        except Exception as e:
            if not isinstance(e, urllib.error.HTTPError):
                cnt += 1
                if cnt <= args.max_retries:
                    continue
            if isinstance(e, urllib.error.HTTPError):
                result["status"] = "expired"
            else:
                result["status"] = "timeout"
        break
    return result


def main():
    start = time.time()
    if os.path.exists(args.output_folder) and os.listdir(args.output_folder):
        try:
            c = input(
                f"'{args.output_folder}' already exists and is not an empty directory, continue? (y/n) "
            )
            if c.lower() not in ["y", "yes"]:
                exit(0)
        except KeyboardInterrupt:
            exit(0)
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    image_folder_path = os.path.join(args.output_folder, "images")
    record_path = os.path.join(args.output_folder, "records.json")
    record = {'success': [], 'expired': [], 'timeout': []}
    if os.path.isfile(record_path):
        try:
            with open(record_path, encoding="utf8") as f:
                record['success'] = json.load(f)['success']
        except:
            pass
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)

    list_url = 'https://raw.githubusercontent.com/V3Det/v3det_resource/main/resource/download_list.txt'
    response = urllib.request.urlopen(urllib.request.Request(url=list_url, headers=headers), timeout=10)
    url_list = [url for url in response.read().decode('utf-8').split('\n') if len(url) > 0]
    image2url = {}
    for url in url_list:
        response = urllib.request.urlopen(urllib.request.Request(url=url, headers=headers), timeout=10)
        image2url.update(eval(response.read().decode('utf-8')))

    data = []
    rec_suc = set(record['success'])
    for image, url in image2url.items():
        if image not in rec_suc:
            data.append((url, image))
    with tqdm(total=len(data)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            # Submit up to `chunk_size` tasks at a time to avoid too many pending tasks.
            chunk_size = min(5000, args.max_workers * 500)
            for i in range(0, len(data), chunk_size):
                futures = [
                    executor.submit(download_image, url, path, 10)
                    for url, path in data[i: i + chunk_size]
                ]
                for future in concurrent.futures.as_completed(futures):
                    r = future.result()
                    record[r["status"]].append(r["path"])
                    pbar.update(1)
                with open(record_path, "w", encoding="utf8") as f:
                    json.dump(record, f, indent=2)

    end = time.time()
    print(f"consuming time {end - start:.1f} sec")
    print(f"{len(record['success'])} images downloaded.")
    print(f"{len(record['timeout'])} urls failed due to request timeout.")
    print(f"{len(record['expired'])} urls failed due to url expiration.")
    if len(record['success']) == len(image2url):
        os.remove(record_path)
        print('All images have been downloaded!')
    else:
        print('Please run this file again to download failed image!')


if __name__ == "__main__":
    main()
