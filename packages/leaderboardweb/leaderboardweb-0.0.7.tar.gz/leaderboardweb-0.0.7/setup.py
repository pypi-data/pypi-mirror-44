import setuptools

VERSION = "0.0.7"

setuptools.setup(
    name="leaderboardweb",
    packages=setuptools.find_packages(),
    package_data={"leaderboardweb": ["static/*", "static/images/*", "static/static/js/*", "static/static/css/*"]},
    version=VERSION,
    description="Frontend for All Inspiration Clan Leaderboard",
    author="Hugo Wainwright",
    author_email="wainwrighthugo@gmail.com",
    url="https://github.com/frugs/allin-web",
    keywords=["sc2", "MMR"],
    classifiers=[],
    install_requires=["flask"],
)
