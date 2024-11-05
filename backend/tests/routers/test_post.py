from http.client import responses

import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts", json={"body": body})
    return response.json()

async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post("/comments", json={"body": body, "post_id": post_id})
    return response.json()

@pytest.fixture
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)

@pytest.fixture
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test Comment", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"
    response = await async_client.post(
        "/posts",
        json={"body": body},
    )
    assert response.status_code == 201
    assert {"id": 0, "body": "Test Post"}.items() <= response.json().items()


@pytest.mark.anyio
async def test_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/posts", json={})
    assert response.status_code == 422

@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/posts")
    assert response.status_code == 200
    assert created_post in response.json()


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    response = await async_client.post(
        "/comments",
        json={"body": "Test Comment", "post_id": created_post["id"]},
    )
    assert response.status_code == 201
    assert {"id": 0, "body": "Test Comment", "post_id": created_post["id"]}.items() <= response.json().items()

@pytest.mark.anyio
async def test_get_comments_on_post(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/posts/{created_post['id']}/comments")
    assert response.status_code == 200
    assert response.json() == [created_comment]

@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/posts/{created_post['id']}/with-comments")
    assert response.status_code == 200
    assert response.json() == {
        "post": created_post,
        "comments": [created_comment],
    }

@pytest.mark.anyio
async def test_get_missing_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get("/posts/2")
    assert response.status_code == 404