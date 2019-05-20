# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20190518001052) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "consumptions", force: :cascade do |t|
    t.datetime "time"
    t.integer "consumption"
    t.bigint "vehicle_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["vehicle_id"], name: "index_consumptions_on_vehicle_id"
  end

  create_table "demand_predictions", force: :cascade do |t|
    t.decimal "value"
    t.datetime "datetime"
    t.string "sector"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "owners", force: :cascade do |t|
    t.string "name"
    t.bigint "vehicle_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["vehicle_id"], name: "index_owners_on_vehicle_id"
  end

  create_table "price_predictions", force: :cascade do |t|
    t.decimal "price"
    t.datetime "datetime"
    t.string "sector"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "vehicles", force: :cascade do |t|
    t.string "name"
    t.string "address"
    t.string "charging_sector"
    t.integer "battery_capacity"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "owner_id"
    t.decimal "latitude"
    t.decimal "longitude"
    t.index ["owner_id"], name: "index_vehicles_on_owner_id"
  end

  add_foreign_key "consumptions", "vehicles"
  add_foreign_key "owners", "vehicles"
  add_foreign_key "vehicles", "owners"
end
