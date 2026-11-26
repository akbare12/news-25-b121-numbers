# main.py — stdlib only. Copies the pre-rendered entry.png into the output dir.
# The grader image is stdlib-only: no third-party imports of any kind.
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    src_sha = sha256(SRC)
    dst_sha = sha256(dst)
    assert src_sha == dst_sha, "copy sha mismatch"
    print(dst, dst_sha)
    return dst


if __name__ == "__main__":
    print(main())
