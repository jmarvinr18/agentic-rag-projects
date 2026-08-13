FROM langchain/langgraph-api:3.11

# -- Installing dependencies from uv.lock --
ADD pyproject.toml /tmp/uv_export/project/pyproject.toml
ADD uv.lock /tmp/uv_export/project/uv.lock
WORKDIR /tmp/uv_export/project
RUN uv export --package lwa-agent --frozen --no-hashes --no-emit-project --no-emit-workspace -o uv_requirements.txt
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -c /api/constraints.txt -r uv_requirements.txt
RUN rm -rf /tmp/uv_export
# -- End of uv.lock dependencies install --

# -- Adding workspace package . --
ADD .cache /deps/workspace/.cache
ADD .env /deps/workspace/.env
ADD .flaskenv /deps/workspace/.flaskenv
ADD .python-version /deps/workspace/.python-version
ADD README.md /deps/workspace/README.md
ADD app /deps/workspace/app
ADD app.py /deps/workspace/app.py
ADD langgraph.json /deps/workspace/langgraph.json
ADD pyproject.toml /deps/workspace/pyproject.toml
ADD requirements.txt /deps/workspace/requirements.txt
ADD test_graph.py /deps/workspace/test_graph.py
ADD uv.lock /deps/workspace/uv.lock
WORKDIR /deps/workspace
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir -c /api/constraints.txt --no-deps -e .
# -- End of workspace package . --

ENV LANGSERVE_GRAPHS='{"agent_graph": {"path": "app.graphs.builder:graph"}}'

# -- Ensure user deps didn't inadvertently overwrite langgraph-api
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license && touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py
RUN PYTHONDONTWRITEBYTECODE=1 uv pip install --system --no-cache-dir --no-deps -e /api
# -- End of ensuring user deps didn't inadvertently overwrite langgraph-api --
# -- Removing build deps from the final image ~<:===~~~ --
RUN pip uninstall -y pip setuptools wheel
RUN rm -rf /usr/local/lib/python*/site-packages/pip* /usr/local/lib/python*/site-packages/setuptools* /usr/local/lib/python*/site-packages/wheel* && find /usr/local/bin -name "pip*" -delete || true
RUN rm -rf /usr/lib/python*/site-packages/pip* /usr/lib/python*/site-packages/setuptools* /usr/lib/python*/site-packages/wheel* && find /usr/bin -name "pip*" -delete || true
RUN uv pip uninstall --system pip setuptools wheel && rm /usr/bin/uv /usr/bin/uvx

WORKDIR /deps/workspace