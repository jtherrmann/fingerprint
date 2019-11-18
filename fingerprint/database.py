import os
from collections import Counter

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


def add_fingerprint(
        fingerprint_type, user_id, collection_datetime, headers, js_data=None):
    session = Session()
    try:
        row_kwargs = get_row_kwargs(headers, js_data)

        session.add(
            fingerprint_type(
                cookie_user_id=user_id,
                collection_datetime=collection_datetime,
                **row_kwargs
            )
        )
        session.commit()

        results = dict()

        results['overall_similarity'] = overall_similarity(
            session, fingerprint_type, row_kwargs
        )

        results['headers_results'] = list(
            similarity_results(
                session, fingerprint_type, headers, header_to_column_name
            )
        )

        if js_data is not None:
            results['js_data_results'] = list(
                similarity_results(
                    session, fingerprint_type, js_data, js_data_to_column_name
                )
            )

        return results
    except:  # noqa: E722
        session.rollback()
        raise
    finally:
        session.close()


def similarity_results(session, fingerprint_type, attrs, column_name_func):
    total = session.query(fingerprint_type).count()
    for k, v in attrs:
        col_name = column_name_func(k)
        count = session\
            .query(fingerprint_type)\
            .filter_by(**{col_name: v})\
            .count()
        percentage = get_percentage(count, total)
        yield k, v, percentage


def overall_similarity(session, fingerprint_type, row_kwargs):
    total = session.query(fingerprint_type).count()
    count = session.query(fingerprint_type).filter_by(**row_kwargs).count()
    return get_percentage(count, total)


def get_percentage(count, total):
    return f'{round(count/total*100, 2)}%'


def get_row_kwargs(headers, js_data):
    kwargs = headers_to_row_kwargs(headers)
    kwargs.update(js_data_to_row_kwargs(js_data))
    return kwargs


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


def get_stats(fingerprint_type):
    columns = fingerprint_type.__table__.columns.keys()
    stats = {col: Counter() for col in columns}
    session = Session()
    try:
        rows = session.query(fingerprint_type)
        for row in rows:
            for col in columns:
                value = getattr(row, col)
                stats[col][value] += 1
        return stats
    finally:
        session.close()
