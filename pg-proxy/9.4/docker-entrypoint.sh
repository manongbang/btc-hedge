#!/bin/bash
set -e

function init_pgbouncer()
{
	POSTGRESQL_USER=${POSTGRES_USER:-}
	POSTGRESQL_PASSWORD=${POSTGRES_PASSWORD:-}
	POSTGRESQL_READONLY_USER=${POSTGRES_READONLY_USER:-}
	POSTGRESQL_READONLY_PASSWORD=${POSTGRES_READONLY_PASSWORD:-}
	POSTGRESQL_MAX_CLIENT_CONN=${POSTGRES_MAX_CLIENT_CONN:-}
	POSTGRESQL_DEFAULT_POOL_SIZE=${POSTGRES_DEFAULT_POOL_SIZE:-}
	POSTGRESQL_SERVER_LIFETIME=${POSTGRES_SERVER_LIFETIME:-}
	POSTGRESQL_SERVER_IDLE_TIMEOUT=${POSTGRES_SERVER_IDLE_TIMEOUT:-}
	POSTGRESQL_SERVER_CONNECT_TIMEOUT=${POSTGRES_SERVER_CONNECT_TIMEOUT:-}

	#if [ ! -f /etc/pgbouncer/pgbouncer.ini ]
	#then
		cat > /etc/pgbouncer/pgbouncer.ini <<-EOF
		[databases]
		* = host=localhost port=5432

		[pgbouncer]
		logfile = /var/log/postgresql/pgbouncer.log
		pidfile = /var/run/postgresql/pgbouncer.pid
		;listen_addr = *
		listen_addr = 0.0.0.0
		listen_port = 5433
		unix_socket_dir = /var/run/postgresql
		;auth_type = any
		auth_type = md5
		auth_file = /etc/pgbouncer/userlist.txt
		admin_users = admin
		stats_users = admin
		pool_mode = session
		server_reset_query = DISCARD ALL
		max_client_conn = ${POSTGRESQL_MAX_CLIENT_CONN}
		default_pool_size = ${POSTGRESQL_DEFAULT_POOL_SIZE}
		ignore_startup_parameters = extra_float_digits
		server_lifetime = ${POSTGRESQL_SERVER_LIFETIME}
		server_idle_timeout = ${POSTGRESQL_SERVER_IDLE_TIMEOUT}
		server_connect_timeout = ${POSTGRESQL_SERVER_CONNECT_TIMEOUT}
		tcp_keepalive = 1
		tcp_keepcnt = 2
		tcp_keepidle = 120
		tcp_keepintvl = 15
		EOF
	#fi

	if [ ! -s /etc/pgbouncer/userlist.txt ]
	then
			echo '"'"${POSTGRESQL_USER}"'" "'"${POSTGRESQL_PASSWORD}"'"'  > /etc/pgbouncer/userlist.txt
            if [[ "$POSTGRES_READONLY_USER" && "$POSTGRES_READONLY_PASSWORD" ]]; then
			    echo '"'"${POSTGRESQL_READONLY_USER}"'" "'"${POSTGRESQL_READONLY_PASSWORD}"'"'  >> /etc/pgbouncer/userlist.txt
            fi
			echo '"'"admin"'" "'"${POSTGRESQL_PASSWORD}"'"'  >> /etc/pgbouncer/userlist.txt
	fi

	chown -R postgres:postgres /etc/pgbouncer
	chown root:postgres /var/log/postgresql
	chmod 1775 /var/log/postgresql
	chmod 640 /etc/pgbouncer/userlist.txt
}


if [ "${1:0:1}" = '-' ]; then
	set -- postgres "$@"
fi

if [ "$1" = 'postgres' ]; then
	mkdir -p "$PGDATA"
	chmod 700 "$PGDATA"
	chown -R postgres "$PGDATA"

	chmod g+s /run/postgresql
	chown -R postgres /run/postgresql

	# look specifically for PG_VERSION, as it is expected in the DB dir
	if [ ! -s "$PGDATA/PG_VERSION" ]; then
		eval "gosu postgres initdb $POSTGRES_INITDB_ARGS"

		# check password first so we can output the warning before postgres
		# messes it up
		if [ "$POSTGRES_PASSWORD" ]; then
			pass="PASSWORD '$POSTGRES_PASSWORD'"
			readonly_pass="PASSWORD '$POSTGRES_READONLY_PASSWORD'"
			authMethod=md5
		else
			# The - option suppresses leading tabs but *not* spaces. :)
			cat >&2 <<-'EOWARN'
				****************************************************
				WARNING: No password has been set for the database.
						 This will allow anyone with access to the
						 Postgres port to access your database. In
						 Docker's default configuration, this is
						 effectively any other container on the same
						 system.
						 Use "-e POSTGRES_PASSWORD=password" to set
						 it in "docker run".
				****************************************************
			EOWARN

			pass=
			readonly_pass=
			authMethod=trust
		fi

		{ echo; echo "host all all 0.0.0.0/0 $authMethod"; } >> "$PGDATA/pg_hba.conf"

		# internal start of server in order to allow set-up using psql-client
		# does not listen on external TCP/IP and waits until start finishes
		gosu postgres pg_ctl -D "$PGDATA" \
			-o "-c listen_addresses='localhost'" \
			-w start

		: ${POSTGRES_USER:=postgres}
		: ${POSTGRES_DB:=$POSTGRES_USER}
		export POSTGRES_USER POSTGRES_DB

		psql=( psql -v ON_ERROR_STOP=1 )

		if [ "$POSTGRES_DB" != 'postgres' ]; then
			"${psql[@]}" --username postgres <<-EOSQL
				CREATE DATABASE "$POSTGRES_DB" ;
			EOSQL
			echo "created databse $POSTGRES_DB"
		fi

		if [ "$POSTGRES_USER" = 'postgres' ]; then
			op='ALTER'
		else
			op='CREATE'
		fi
		"${psql[@]}" --username postgres <<-EOSQL
			$op USER "$POSTGRES_USER" WITH SUPERUSER $pass ;
		EOSQL
		echo "created user ${POSTGRES_USER}"

		psql+=( --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" )
        echo
        if [[ "$POSTGRES_READONLY_USER" && "$POSTGRES_READONLY_PASSWORD" ]]; then
            # add read-only user
            "${psql[@]}" --username postgres <<-EOSQL
		    	CREATE USER "$POSTGRES_READONLY_USER" WITH $readonly_pass ;
                GRANT CONNECT ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_READONLY_USER" ;
                GRANT USAGE ON SCHEMA public TO "$POSTGRES_READONLY_USER" ;
                GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO "$POSTGRES_READONLY_USER" ;
                GRANT SELECT ON ALL TABLES IN SCHEMA public TO "$POSTGRES_READONLY_USER" ;
                ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "$POSTGRES_READONLY_USER" ;
                ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO "$POSTGRES_READONLY_USER" ;
			EOSQL
		    echo "created read-only user ${POSTGRES_READONLY_USER}"
        fi

		for f in /docker-entrypoint-initdb.d/*; do
			case "$f" in
				*.sh)	 echo "$0: running $f"; . "$f" ;;
				*.sql)	echo "$0: running $f"; "${psql[@]}" < "$f"; echo ;;
				*.sql.gz) echo "$0: running $f"; gunzip -c "$f" | "${psql[@]}"; echo ;;
				*)		echo "$0: ignoring $f" ;;
			esac
		done
		gosu postgres pg_ctl -D "$PGDATA" -m fast -w stop

		echo
		echo 'PostgreSQL init process complete; ready for start up.'
		echo
	fi

	init_pgbouncer
	gosu postgres pgbouncer -d -v /etc/pgbouncer/pgbouncer.ini

	exec gosu postgres "$@"
fi

exec "$@"

