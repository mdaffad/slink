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
	redisclient *redis.Client
)

func init() {

	// ? Load the .env variables
	config, err := configs.LoadConfig(".")
	if err != nil {
		log.Fatal("Could not load environment variables", err)
	}
}
func main() {
}
