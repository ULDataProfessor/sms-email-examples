"""Compare high level configuration between Redshift (cloud) and PostgreSQL (on-prem)."""


def redshift_config():
    return {
        "host": "redshift.amazonaws.com",
        "port": 5439,
        "user": "admin",
        "password": "<secret>",
        "extra": "Uses AWS-managed cluster",
    }


def postgres_config():
    return {
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "<secret>",
        "extra": "Self-managed hardware",
    }


def main() -> None:
    print("Cloud Redshift config:\n", redshift_config())
    print("On-prem PostgreSQL config:\n", postgres_config())


if __name__ == "__main__":
    main()

