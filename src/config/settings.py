from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PROJECT
    LOCAL: bool = True
    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = ['*']
    # POSTGRES
    DB_NAME: str = ''
    DB_HOST: str = ''
    DB_PORT: int = 5432
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''

    def get_postgres_dsn(self, is_async=True, **options):
        """
        Return DSN for postgresql from options,
        if options is not passed then default option takes from config.
        """
        driver = 'asyncpg' if is_async else 'psycopg2'
        return 'postgresql+{driver}://{user}:{password}@{host}:{port}/{database}'.format(
            driver=driver,
            user=options.get(
                'user',
                self.POSTGRES_USER
            ),
            password=options.get(
                'password',
                self.POSTGRES_PASSWORD
            ),
            host=options.get(
                'host',
                self.DB_HOST
            ),
            port=options.get(
                'port',
                self.DB_PORT
            ),
            database=options.get('database', self.DB_NAME),
        )
