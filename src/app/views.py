from flask import Blueprint
from yarl import URL
from flask import Flask, render_template, redirect, url_for, request, make_response
from .forms import APIKeyForm,SearchForm
from ..notion_helpers import *
notion_admin = Blueprint('notion_admin', __name__)



@notion_admin.route("/", methods = ['POST', 'GET'])
def home():
    # redirect to setcookie if no name is present in the cookie
    NOTION_API_KEY = request.cookies.get('NotionAPIKey')
    # todo: refactor this
    if not NOTION_API_KEY:
      api_form = APIKeyForm()
      if api_form.validate_on_submit():
        NOTION_API_KEY = str(api_form.api_key.data)
        resp = make_response(redirect("/"))

        resp.set_cookie('NotionAPIKey', NOTION_API_KEY)
        return resp
      return render_template('submit_form.html',form = api_form)

    NOTION_PAGE_ID = request.cookies.get('NotionPageID') # store list of notion_page_id #jsonify if neccesary
    if not NOTION_PAGE_ID:
      return redirect("/searchpages")
    if NOTION_API_KEY and NOTION_PAGE_ID:

      return redirect(url_for('add_viewer'))

      # list all the pages that were added
      # click on page to go tot the page in notion # with newtab

      # in notion add an embedpage block which point towards /redirect(/viewer) and make a get request with the notion_page_id as an param
      # if this get request is saved as the url, it will always stay in that page
      # or instead of a get request use a variable route /view/$page_id$




@notion_admin.route('/searchpages',methods=['GET','POST'])
def searchpages():

  search_form = SearchForm()
  NOTION_API_KEY = request.cookies.get('NotionAPIKey')
  search_form.page_id.choices = notion_pages_tuple(NOTION_API_KEY)
  if search_form.validate_on_submit():
    NOTION_PAGE_ID = str(search_form.page_id.data)
    resp = make_response(redirect("/"))
    resp.set_cookie('NotionPageID', NOTION_PAGE_ID)
    return resp
  return render_template('submit_form.html',form = search_form)

@notion_admin.route('/add_viewer')
def add_viewer():
  import notional
  from notional.records import Page

  NOTION_TOKEN = request.cookies.get('NotionAPIKey')
  page_id = request.cookies.get('NotionPageID')
  embed_url = URL(request.base_url).with_path(f'viewer/{page_id}')


  notion = notional.connect(auth=NOTION_TOKEN)

  parent_page = notion.pages.retrieve(page_id)

  page = notion.pages.create(
      parent=parent_page, 
      title="News Map")

  from notional.blocks import NestedObject, Embed

  class NestedData(NestedObject):
      url: str

  notion.blocks.children.append(
      page,
      Embed(embed = NestedData(url=embed_url))
  )
  return ''

  # if a get request is made, this means the page is requested without submitting the form, therefore show all pages which are shared with the integration
  # query = request.

@notion_admin.route('/viewer/<page_id>')
def viewer(page_id):
    # dash_app = Dash(__name__, external_stylesheets=external_stylesheets, server=app)

    # dash_app.layout = html.Div(children=[

    #     dcc.Graph(
    #         id='news-table',
    #         figure=NewsTable(news_df).figure()
    #     )
    # ])


    # return dash_app.index
    return f'this is page number {page_id}'