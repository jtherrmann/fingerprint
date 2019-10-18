import os
import traceback

import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# `DATABASE_URL` is set by Heroku.
ENGINE = sqlalchemy.create_engine(os.environ['DATABASE_URL'])

Base = declarative_base()


class InitialRequestFingerprint(Base):
    __tablename__ = "initial_request_fingerprints"
    id = Column(Integer, primary_key=True)
    cookie_user_id = Column(String)
    collection_datetime = Column(DateTime)
    user_agent = Column(String)
    accept = Column(String)
    accept_language = Column(String)
    accept_encoding = Column(String)
    dnt = Column(String)
    upgrade_insecure_requests = Column(String)


class JavaScriptFingerprint(Base):
    __tablename__ = "javascript_fingerprints"
    id = Column(Integer, primary_key=True)
    cookie_user_id = Column(String)
    collection_datetime = Column(DateTime)
    user_agent = Column(String)
    accept_language = Column(String)
    accept_encoding = Column(String)
    dnt = Column(String)
    timezone_offset = Column(String)


Base.metadata.create_all(ENGINE)

Session = sessionmaker()

Session.configure(bind=ENGINE)


# TODO propagate exceptions to caller
def add_fingerprint(
        fingerprint_type, user_id, collection_datetime, headers, js_data=None):
    session = Session()
    try:
        session.add(
            fingerprint_type(
                cookie_user_id=user_id,
                collection_datetime=collection_datetime,
                **headers_to_row_kwargs(headers),
                **js_data_to_row_kwargs(js_data)
            )
        )
        session.commit()

        # TODO temp
        return [(k, v, '25%') for k, v in headers]
    except:  # noqa: E722
        print(traceback.format_exc())
        session.rollback()
    finally:
        session.close()


def headers_to_row_kwargs(headers):
    return {header_to_column_name(k): v for k, v in headers}


def header_to_column_name(key):
    return key.lower().replace('-', '_')


def js_data_to_row_kwargs(js_data):
    return {} if js_data is None \
        else {js_data_to_column_name(k): v for k, v in js_data}


def js_data_to_column_name(key):
    return key.lower().replace(' ', '_')


def cookie_id_already_exists(cookie_id):
    session = Session()
    try:
        return session\
            .query(InitialRequestFingerprint)\
            .filter_by(cookie_user_id=cookie_id)\
            .count() > 0
    finally:
        session.close()
