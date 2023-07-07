package configs

import "os"

type Config struct {
	RedisURL string
	Port     string
}

func LoadConfig() (config Config, err error) {
	ok := false
	config.RedisURL, ok = os.LookupEnv("REDIS_URL")
	if !ok {
		config.RedisURL = "localhost:6379"
	}

	config.Port, ok = os.LookupEnv("PORT")
	if !ok {
		config.Port = "8888"
	}

	return
}
