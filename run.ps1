# PowerShell Helper Script for Solar Big Data Pipeline

param (
    [string]$Command = "up"
)

switch ($Command) {
    "up" {
        docker compose up -d --build
    }
    "down" {
        docker compose down -v
    }
    "init" {
        docker compose exec namenode /bin/bash /scripts/hdfs_init.sh
        docker compose exec hive /bin/bash /scripts/hive_init.sh
    }
    "dev-sample" {
        python scripts/make_dev_sample.py
    }
    "test-backend" {
        pytest backend/tests/
    }
    "test-frontend" {
        npm --prefix frontend test
    }
    default {
        Write-Host "Usage: .\run.ps1 [up|down|init|dev-sample|test-backend|test-frontend]"
    }
}
