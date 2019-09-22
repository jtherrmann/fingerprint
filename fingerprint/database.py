import configparser
import os

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def parse_config_file():
    name = 'database.cfg'
    assert os.path.isfile(name), f'{name} is not a file'
    config = configparser.ConfigParser()
    config.read(name)
    return dict(config['default'])


CFG = parse_config_file()

ENGINE = sqlalchemy.create_engine(
    f"postgresql://{CFG['username']}:{CFG['password']}"
    f"@{CFG['hostname']}/{CFG['dbname']}"
)

Base = declarative_base()


class InitialRequestFingerprint(Base):
    __tablename__ = "initial_request_fingerprints"
    id = Column(Integer, primary_key=True)
    user_agent = Column(String)
    accept = Column(String)
    accept_language = Column(String)
    accept_encoding = Column(String)
    dnt = Column(String)
    upgrade_insecure_requests = Column(String)


class JavaScriptFingerprint(Base):
    __tablename__ = "javascript_fingerprints"
    id = Column(Integer, primary_key=True)
    user_agent = Column(String)
    accept_language = Column(String)
    accept_encoding = Column(String)
    dnt = Column(String)
    timezone_offset = Column(String)


Base.metadata.create_all(ENGINE)

Session = sessionmaker()

Session.configure(bind=ENGINE)


def add_initial_request_fingerprint(headers):
    session = Session()
    try:
        session.add(get_initial_request_fingerprint(headers))
        session.commit()
    except:  # noqa: E722
        # TODO log error
        session.rollback()
    finally:
        session.close()


def get_initial_request_fingerprint(headers):
    return InitialRequestFingerprint(**headers_to_row_kwargs(headers))


def add_javascript_fingerprint(headers, other_data):
    session = Session()
    try:
        session.add(get_javascript_fingerprint(headers, other_data))
        session.commit()
    except:  # noqa: E722
        # TODO log error
        session.rollback()
    finally:
        session.close()


def get_javascript_fingerprint(headers, other_data):
    return JavaScriptFingerprint(
        **headers_to_row_kwargs(headers),
        **javascript_data_to_row_kwargs(other_data)
    )


def headers_to_row_kwargs(headers):
    return {header_to_column_name(k): v for k, v in headers}


def header_to_column_name(header_key):
    return header_key.lower().replace('-', '_')


def javascript_data_to_row_kwargs(data):
    return {javascript_data_key_to_column_name(k): v for k, v in data}


def javascript_data_key_to_column_name(key):
    return key.lower().replace(' ', '_')
