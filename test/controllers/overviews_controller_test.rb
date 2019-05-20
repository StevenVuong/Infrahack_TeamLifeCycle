require 'test_helper'

class OverviewsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @overview = overviews(:one)
  end

  test "should get index" do
    get overviews_url
    assert_response :success
  end

  test "should get new" do
    get new_overview_url
    assert_response :success
  end

  test "should create overview" do
    assert_difference('Overview.count') do
      post overviews_url, params: { overview: {  } }
    end

    assert_redirected_to overview_url(Overview.last)
  end

  test "should show overview" do
    get overview_url(@overview)
    assert_response :success
  end

  test "should get edit" do
    get edit_overview_url(@overview)
    assert_response :success
  end

  test "should update overview" do
    patch overview_url(@overview), params: { overview: {  } }
    assert_redirected_to overview_url(@overview)
  end

  test "should destroy overview" do
    assert_difference('Overview.count', -1) do
      delete overview_url(@overview)
    end

    assert_redirected_to overviews_url
  end
end
