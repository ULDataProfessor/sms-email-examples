# acid_transactions_test
ACID properties—Atomicity, Consistency, Isolation, Durability—are critical for reliable databases. Testing these guarantees often involves running concurrent transactions and deliberately causing failures. A compliant system should roll back partial changes on errors. This directory illustrates how to simulate such a scenario with DataFrames.
