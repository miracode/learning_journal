import lettuce

from flask import url_for
from journal import app
from journal import init_db
from test_journal import clear_db
from test_journal import TEST_DSN


@lettuce.before.all
def setup_app():
    print "This happens before all the lettuce tests begin"
    app.config['DATABASE'] = TEST_DSN
    app.config['TESTING'] = True

    init_db()


@lettuce.after.all
def teardown_app(total):
    print "This happens after all the lettuce tests have run"
    clear_db()


@lettuce.step('an anonymous user')
def anonymous_user(step):
    with app.test_client() as client:
        lettuce.world.client = client


@lettuce.step('an authenticated user')
def authenticated_user(step):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = True
        lettuce.world.client = client


@lettuce.step('I view the home page')
def request_homepage(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    lettuce.world.response = lettuce.world.client.get(home_url)


@lettuce.step('I do not see the edit button')
def no_edit_button(step):
    body = lettuce.world.response.data
    msg = "found edit_button in %s"
    assert 'class="edit_button"' not in body, msg % body


@lettuce.step('I see the edit button')
def yes_edit_button(step):
    body = lettuce.world.response.data
    msg = "found edit_button in %s"
    assert 'class="edit_button"' in body, msg % body


@lettuce.step('the title "([^"]*)"')
def title_input(step, title):
    lettuce.world.title = title


@lettuce.step('the text "([^"]*)"')
def text_input(step, text):
    lettuce.world.text = text


@lettuce.step('I submit the edited form')
def edit_entry(step):
    entry_data = {
        'title': lettuce.world.title,
        'text': lettuce.world.text
    }
    lettuce.world.response = lettuce.world.client.post(
        '/add', data=entry_data, follow_redirects=False
    )


@lettuce.step('I am redirected to the home page')
def redirected_home(step):
    with app.test_request_context('/'):
        home_url = url_for('show_entries')
    # assert that we have been redirected to the home page
    assert lettuce.world.response.status_code in [301, 302]
    assert lettuce.world.response.location == 'http://localhost' + home_url
    # now fetch the homepage so we can finish this off
    lettuce.world.response = lettuce.world.client.get(home_url)


@lettuce.step('I do not see an edited entry')
def no_edited_entry(step):
    body = lettuce.world.response.data
    for val in [lettuce.world.title, lettuce.world.text]:
        assert val not in body


@lettuce.step('I see the edited entry')
def yes_edited_entry(step):
    body = lettuce.world.response.data
    for val in [lettuce.world.title, lettuce.world.text]:
        assert val in body
