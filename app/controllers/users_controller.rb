class Api::V1::UsersController < ApplicationController

    swagger_controller :users, "User Management"
  
    swagger_api :index do
      summary "Fetches all User items"
      notes "This lists all the active users"
      param :query, :page, :integer, :optional, "Page number"
      param :path, :nested_id, :integer, :optional, "Team Id"
      response :unauthorized
      response :not_acceptable, "The request you made is not acceptable"
      response :requested_range_not_satisfiable
    end
  
    swagger_api :show do
      summary "Fetches a single User item"
      param :path, :id, :integer, :optional, "User Id"
      response :ok, "Success", :User
      response :unauthorized
      response :not_acceptable
      response :not_found
    end
  
    swagger_api :create do
      summary "Creates a new User"
      param :form, :first_name, :string, :required, "First name"
      param :form, :last_name, :string, :required, "Last name"
      param :form, :email, :string, :required, "Email address"
      param_list :form, :role, :string, :required, "Role", [ "admin", "superadmin", "user" ]
      response :unauthorized
      response :not_acceptable
    end
  
    swagger_api :update do
      summary "Updates an existing User"
      param :path, :id, :integer, :required, "User Id"
      param :form, :first_name, :string, :optional, "First name"
      param :form, :last_name, :string, :optional, "Last name"
      param :form, :email, :string, :optional, "Email address"
      param :form, :tag, :Tag, :required, "Tag object"
      response :unauthorized
      response :not_found
      response :not_acceptable
    end
  
    swagger_api :destroy do
      summary "Deletes an existing User item"
      param :path, :id, :integer, :optional, "User Id"
      response :unauthorized
      response :not_found
    end
  
    # Support for Swagger complex types:
    # https://github.com/wordnik/swagger-core/wiki/Datatypes#wiki-complex-types
    swagger_model :Tag do
      description "A Tag object."
      property :id, :integer, :required, "User Id"
      property :name, :string, :optional, "Name"
      property_list :type, :string, :optional, "Tag Type", ["info", "warning", "error"]
    end
  end