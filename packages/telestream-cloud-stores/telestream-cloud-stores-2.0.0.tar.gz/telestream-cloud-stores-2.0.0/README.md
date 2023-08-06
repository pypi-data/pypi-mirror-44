# Telestream Cloud Stores Service Python SDK

This library provides a low-level interface to the REST API of Telestream Cloud, the online video encoding service.

## Requirements.

Python 2.7 and 3.4+

## Getting Started

## Documentation for API Endpoints

All URIs are relative to *https://api.cloud.telestream.net/stores/v1.1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*StoresApi* | [**create_store**](docs/StoresApi.md#create_store) | **POST** /stores | 
*StoresApi* | [**create_store_client_link**](docs/StoresApi.md#create_store_client_link) | **POST** /stores/{store_id}/service/{service_name}/id/{service_id} | 
*StoresApi* | [**create_watch_rule**](docs/StoresApi.md#create_watch_rule) | **POST** /watch_rules | 
*StoresApi* | [**delete_store**](docs/StoresApi.md#delete_store) | **DELETE** /stores/{id} | 
*StoresApi* | [**delete_store_client_link**](docs/StoresApi.md#delete_store_client_link) | **DELETE** /stores/{store_id}/service/{service_name}/id/{service_id} | 
*StoresApi* | [**delete_watch_rule**](docs/StoresApi.md#delete_watch_rule) | **DELETE** /watch_rules/{id} | 
*StoresApi* | [**get_object_url**](docs/StoresApi.md#get_object_url) | **GET** /stores/{id}/object_url | 
*StoresApi* | [**get_store**](docs/StoresApi.md#get_store) | **GET** /stores/{id} | 
*StoresApi* | [**get_store_ids_for_client**](docs/StoresApi.md#get_store_ids_for_client) | **GET** /stores/service/{service_name}/id/{service_id} | 
*StoresApi* | [**get_stores**](docs/StoresApi.md#get_stores) | **GET** /stores | 
*StoresApi* | [**get_watch_rule**](docs/StoresApi.md#get_watch_rule) | **GET** /watch_rules/{id} | 
*StoresApi* | [**get_watch_rules**](docs/StoresApi.md#get_watch_rules) | **GET** /watch_rules | 
*StoresApi* | [**sync_watch_rule**](docs/StoresApi.md#sync_watch_rule) | **POST** /watch_rules/{id}/sync | 
*StoresApi* | [**update_store**](docs/StoresApi.md#update_store) | **PATCH** /stores/{id} | 
*StoresApi* | [**update_watch_rule**](docs/StoresApi.md#update_watch_rule) | **PATCH** /watch_rules/{id} | 
*StoresApi* | [**validate_bucket**](docs/StoresApi.md#validate_bucket) | **POST** /validate_bucket | 


## Documentation For Models

 - [AlternativePathFormat](docs/AlternativePathFormat.md)
 - [Error](docs/Error.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [ObjectURL](docs/ObjectURL.md)
 - [Output](docs/Output.md)
 - [Store](docs/Store.md)
 - [StoreBody](docs/StoreBody.md)
 - [StoreBodyProviderSpecificSettings](docs/StoreBodyProviderSpecificSettings.md)
 - [ValidateBucketBody](docs/ValidateBucketBody.md)
 - [ValidateBucketResponse](docs/ValidateBucketResponse.md)
 - [WatchRule](docs/WatchRule.md)


## Documentation For Authorization


## api_key

- **Type**: API key
- **API key parameter name**: X-Api-Key
- **Location**: HTTP header


## Author

you@your-company.com

