import pandas as pd
import pytest

from ..main import main, read_input, ValidationError


def test_missing_file(tmp_path, caplog):
    missing = tmp_path / 'nope.csv'
    caplog.set_level('ERROR')
    main(str(missing), str(tmp_path / 'out.json'))
    assert any('Validation error' in r.message for r in caplog.records)


def test_invalid_data(tmp_path):
    bad = tmp_path / 'bad.csv'
    bad.write_text('foo\n1')
    with pytest.raises(ValidationError):
        read_input(bad)


def test_processing_error(tmp_path, caplog):
    data = pd.DataFrame({'age': [1]})
    csv_path = tmp_path / 'input.csv'
    data.to_csv(csv_path, index=False)
    caplog.set_level('ERROR')
    main(str(csv_path), str(tmp_path / 'out.json'))
    assert any('Processing error' in r.message for r in caplog.records)
