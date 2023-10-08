async def insert_user(connection, user_id: int, latitude: float, longitude: float):
    async with connection.cursor() as cursor:
        insert_data = f"INSERT INTO `user` (user_id, latitude, longitude) VALUES ('{user_id}','{latitude}','{longitude}');"
        await cursor.execute(insert_data)
        await connection.commit()


async def update_user_location(connection, user_id: int, latitude: float, longitude: float):
    async with connection.cursor() as cursor:
        update_query = (
            f"UPDATE `user` "
            f"SET latitude = '{latitude}, longitude = '{longitude}'"
            f"WHERE user_id = {user_id}"
        )
        await cursor.execute(update_query)
        await connection.commit()


async def check_user_exists(connection, user_id: int) -> bool:
    async with connection.cursor() as cursor:
        query = f"SELECT COUNT(*) FROM user WHERE user_id = '{user_id}'"
        await cursor.execute(query)
        result = await cursor.fetchone()
        return result[0] > 0
