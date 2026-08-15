from setuptools import setup


setup(
    name="ai-core-framework",
    version="0.5.0",
    description="AI-Core CLI and daily control plane for the phased AI-assisted engineering framework.",
    packages=["ai_core_cli"],
    python_requires=">=3.9",
    entry_points={"console_scripts": ["ai-core=ai_core_cli.main:main"]},
)
