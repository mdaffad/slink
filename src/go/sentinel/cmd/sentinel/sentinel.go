package main

import (
	"context"
	"log"

	"github.com/gin-gonic/gin"
	"github.com/mdaffad/slink/sentinel/configs"
	"github.com/redis/go-redis/v9"
)

var (
	server      *gin.Engine
	ctx         context.Context
	redisClient *redis.Client
)

func init() {

	// ? Load the .env variables
	config, err := configs.LoadConfig()
	if err != nil {
		log.Fatal("Could not load environment variables", err)
	}
	println(config.RedisURL)
	println(config.Port)

	ctx = context.TODO()

	// ? Connect to Redis
	redisClient = redis.NewClient(&redis.Options{
		Addr:     config.RedisURL,
		Password: "admin123",
	})

	if _, err := redisClient.Ping(ctx).Result(); err != nil {
		panic(err)
	}

	if err != nil {
		panic(err)
	}
}

func main() {

}
