# Environment & Setup Guide

## Prerequisites
- Windows 10/11 with Docker Desktop (WSL2 Backend enabled)
- Git (configured for LF line endings)
- Python 3.10+ (for host-side test runner and helper scripts)
- Node.js 18+ & npm (for host-side frontend testing)

## Setup Instructions
1. Clone the repository into WSL2 / local workspace.
2. Copy `.env.example` to `.env`.
3. Download Kaggle dataset or run `python scripts/make_dev_sample.py` to create a sample dataset.
4. Build and start containers: `docker compose up -d --build`.
5. Run cluster init scripts:
   - `docker compose exec namenode /bin/bash /scripts/hdfs_init.sh`
   - `docker compose exec hive /bin/bash /scripts/hive_init.sh`
