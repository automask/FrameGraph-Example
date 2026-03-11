import sys, os, subprocess
from pathlib import Path

root = Path(__file__).parent
root_deps = root / "_deps"
vcpkg_root = root / "vcpkg"
vcpkg_boot = vcpkg_root / "bootstrap-vcpkg.bat"
vcpkg_exe = vcpkg_root / "vcpkg.exe"
dep_list = [
    "catch2",
    "spdlog",
    "glm",
    "glfw3",
    "stb",
    "assimp",
    "imgui",
    "nlohmann-json",
]
dep_repo = [
    {
        "url": "https://github.com/skaarj1989/FrameGraph",
        "tag": "master",
    },
    {
        "url": "https://github.com/skaarj1989/glad",
        "tag": "gl",
    },
    {
        "url": "https://github.com/wolfpld/tracy",
        "tag": "master",
    },
]


def git_clone(url, tag=None, depth=1, recursive=True, cwd=None):
    cmd = ["git", "clone"]
    if tag:
        cmd.append("-b")
        cmd.append(str(tag))
    if depth != None and depth > 0:
        cmd.append("--depth")
        cmd.append(str(depth))
    if recursive:
        cmd.append("--recursive")
    cmd.append(url)
    subprocess.run(cmd, cwd=cwd)


def InstallGitRepo():
    if not root_deps.exists():
        root_deps.mkdir()

    for repo in dep_repo:
        git_clone(**repo, cwd=root_deps)


def InstallPackage():
    if not vcpkg_boot.exists():
        git_clone("https://github.com/microsoft/vcpkg", cwd=root)
    if not vcpkg_exe.exists():
        subprocess.run(vcpkg_boot, cwd=root)

    assert vcpkg_exe.exists()
    subprocess.run(["vcpkg.exe", "install", *dep_list], cwd=vcpkg_root)


InstallPackage()
InstallGitRepo()
