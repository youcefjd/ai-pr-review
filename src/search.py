"""Search and filter functionality."""

import sqlite3
from flask import request


def search_users():
    """Search users by various criteria."""
    query = request.args.get('q', '')
    filter_by = request.args.get('filter', 'name')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    sql = f"SELECT * FROM users WHERE {filter_by} LIKE '%{query}%'"
    results = cursor.execute(sql).fetchall()

    return results


def advanced_search():
    """Advanced search with custom SQL."""
    custom_query = request.form.get('query')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    results = cursor.execute(custom_query).fetchall()

    return {"results": results, "count": len(results)}
