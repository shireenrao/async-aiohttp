import requests
import time


def download_pep(pep_number: int) -> bytes:
    url = f"https://www.python.org/dev/peps/pep-{pep_number}/"
    print(f"Begin downloading {url}")
    response = requests.get(url)
    print(f"Finished downloading {url}")
    return response.content


def write_to_file(pep_number: int, content: bytes) -> None:
    filename = f"sync_{pep_number}.html"
    with open(filename, 'wb') as pep_file:
        print(f"Begin writing {filename}")
        pep_file.write(content)
        print(f"Finished writing {filename}")


if __name__ == '__main__':
    s = time.perf_counter()

    for i in range(8010, 8017):
        content = download_pep(i)
        write_to_file(i, content)

    elapsed = time.perf_counter() - s
    print(f"Execution time: {elapsed:.2f} seconds")

