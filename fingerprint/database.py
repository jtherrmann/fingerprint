import os
from collections import Counter

import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import util


# `DATABASE_URL` is set by Heroku.
ENGINE = sqlalchemy.create_engine(os.environ['DATABASE_URL'])

Base = declarative_base()


class InitialRequestFingerprint(Base):
    __tablename__ = "initial_request_fingerprints"
    id = Column(Integer, primary_key=True)
    cookie_user_id = Column(String)
    collection_datetime = Column(DateTime)
    header_user_agent = Column(String)
    header_accept = Column(String)
    header_accept_language = Column(String)
    header_accept_encoding = Column(String)
    header_dnt = Column(String)
    header_upgrade_insecure_requests = Column(String)


class JavaScriptFingerprint(Base):
    __tablename__ = "javascript_fingerprints"
    id = Column(Integer, primary_key=True)
    cookie_user_id = Column(String)
    collection_datetime = Column(DateTime)
    header_user_agent = Column(String)
    header_accept_language = Column(String)
    header_accept_encoding = Column(String)
    header_dnt = Column(String)
    js_timezone_offset = Column(String)
    js_app_code_name = Column(String)
    js_app_version = Column(String)
    js_build_id = Column(String)
    js_cookies_enabled = Column(String)
    js_do_not_track = Column(String)
    js_hardware_concurrency = Column(String)
    js_java_enabled = Column(String)
    js_language = Column(String)
    js_max_touch_points = Column(String)
    js_platform = Column(String)
    js_plugins = Column(String)
    js_product = Column(String)
    js_product_sub = Column(String)
    js_vendor = Column(String)
    js_vendor_sub = Column(String)
    js_web_driver = Column(String)


Base.metadata.create_all(ENGINE)

Session = sessionmaker()

Session.configure(bind=ENGINE)


def add_fingerprint(
        fingerprint_type, user_id, collection_datetime, headers, js_data=None):
    session = Session()
    try:
        results = dict()

        row_kwargs = get_row_kwargs(headers, js_data)

        if not fingerprint_exists(
                session, fingerprint_type, row_kwargs, user_id):
            session.add(
                fingerprint_type(
                    cookie_user_id=user_id,
                    collection_datetime=collection_datetime,
                    **row_kwargs
                )
            )
            session.commit()
            results['duplicate'] = False
        else:
            results['duplicate'] = True

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


def fingerprint_exists(session, fingerprint_type, row_kwargs, cookie_user_id):
    return session\
        .query(fingerprint_type)\
        .filter_by(cookie_user_id=cookie_user_id, **row_kwargs)\
        .count() > 0


def similarity_results(session, fingerprint_type, attrs, column_name_func):
    total = session.query(fingerprint_type).count()
    for k, v in attrs:
        col_name = column_name_func(k)
        count = session\
            .query(fingerprint_type)\
            .filter_by(**{col_name: v})\
            .count()
        percentage = util.get_percentage(count, total)
        yield k, v, percentage


def overall_similarity(session, fingerprint_type, row_kwargs):
    total = session.query(fingerprint_type).count()
    count = session.query(fingerprint_type).filter_by(**row_kwargs).count()
    return util.get_percentage(count, total)


def get_row_kwargs(headers, js_data):
    kwargs = headers_to_row_kwargs(headers)
    kwargs.update(js_data_to_row_kwargs(js_data))
    return kwargs


def headers_to_row_kwargs(headers):
    return {header_to_column_name(k): v for k, v in headers}


def header_to_column_name(key):
    return 'header_' + key.lower().replace('-', '_')


def js_data_to_row_kwargs(js_data):
    return {} if js_data is None \
        else {js_data_to_column_name(k): v for k, v in js_data}


def js_data_to_column_name(key):
    return 'js_' + key.lower().replace(' ', '_')


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
    columns = [
        col for col in fingerprint_type.__table__.columns.keys()
        if col.startswith('header_') or col.startswith('js_')
    ]
    stats = {col: Counter() for col in columns}
    session = Session()
    try:
        rows = session.query(fingerprint_type)
        for row in rows:
            for col in columns:
                value = getattr(row, col)
                stats[col][value] += 1
        return stats, rows.count()
    finally:
        session.close()
