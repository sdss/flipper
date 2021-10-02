
from flask import url_for

def test_app(client):
    res = client.get(url_for('index.home'))
    assert res.status_code == 200


def test_ok_status(client):
    res = client.get(url_for('index.status'))
    assert res.json == {'flipper status': 'ok'}


def _get_urls(base):
    home = url_for('index.home')
    static = url_for('static', filename='sdss-logo.png')
    assert home == '{0}'.format(base)
    assert static == '{0}static/sdss-logo.png'.format(base)


def test_urls(client):
    ''' test of basic flipper urls '''
    _get_urls('/flipper/')


def test_testbase(testctx):
    ''' test of flipper test server urls '''
    _get_urls('/test/flipper/')
    
    
def test_template(client, get_templates):
    ''' tests accessing a template and context '''
    res = client.get(url_for('index.home'))
    assert res.status_code == 200
    template, context = get_templates[0]
    assert template.name == 'index.html'
    assert context['title'] == 'SDSS Splashpage'


def test_base_release(monkeyrelease, client, get_templates):
    ''' test release changes using main base urls '''
    res = client.get(url_for('index.home'))
    template, context = get_templates[0]
    assert monkeyrelease == context['release']
    url = '{0}.sdss.org'.format(monkeyrelease)
    assert url in context['base_url']
    assert url in context['marvin_url']
    assert 'https://{0}/infrared/'.format(url) in str(res.data)


def test_test_release(testctx, testclient, get_templates):
    ''' tests release changes using the test base url '''
    res = testclient.get(url_for('index.home'))
    template, context = get_templates[0]
    assert 'sas.sdss.org/test' in context['base_url']
    assert 'lore.sdss.utah.edu/test' in context['marvin_url']
    assert 'https://sas.sdss.org/test/infrared/' in str(res.data)

