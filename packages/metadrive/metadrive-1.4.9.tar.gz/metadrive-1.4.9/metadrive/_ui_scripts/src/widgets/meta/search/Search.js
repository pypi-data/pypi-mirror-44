import React, { PureComponent, createRef } from 'react';
import {
  Card,
  CardTitle,
  CardColumns,
  CardSubtitle,
  CardBody,
  Navbar,
  InputGroup,
  Input
} from 'reactstrap';
import ReactMarkdown from 'react-markdown';
import ReactLoading from 'react-loading';
import { Colors } from '@blueprintjs/core';
import MetaContext from '../meta-provider/MetaContext';
import './Search.css';
import 'bootstrap/dist/css/bootstrap.css';

class Search extends PureComponent {
  static contextType = MetaContext;

  static defaultData = {
    search: '',
    results: [],
    status: null
  };

  timeout = null;

  resultsEl = createRef();

  handleChangeSearch = e => {
    if (this.timeout) {
      clearTimeout(this.timeout);
    }

    const search = e.target.value;
    const { setParam } = this.context;
    this.timeout = setTimeout(() => setParam('search', search), 1500);
  };

  handleScroll = () => {
    this.checkUpdating();
  };

  getFirstData = () => {
    const { url, getParam, setData } = this.context;
    const search = getParam('search');

    setData({
      search,
      status: 'loading'
    });
    return fetch(`${url}._filter`, {
      method: 'POST',
      body: JSON.stringify({ search })
    })
      .then(response => response.json())
      .then(({ results, next }) => {
        setData({
          results,
          next,
          status: 'success'
        });
        this.checkUpdating();
      })
      .catch(() => setData({ status: 'error' }));
  };

  getNextData = () => {
    const { getParam, getData, setData } = this.context;
    const { next } = getData(Search.defaultData);
    const search = getParam('search');

    setData({
      status: 'updating'
    });
    return fetch(next, { method: 'POST', body: JSON.stringify({ search }) })
      .then(response => response.json())
      .then(({ results, next }) => {
        setData(data => ({
          results: [...data.results, ...results],
          next,
          status: 'success'
        }));
        this.checkUpdating();
      })
      .catch(() => setData({ status: 'error' }));
  };

  checkUpdating = () => {
    const { getData } = this.context;
    const { status } = getData(Search.defaultData);
    if (status === 'success') {
      const { clientHeight, scrollHeight, scrollTop } = this.resultsEl.current;
      if (scrollTop + clientHeight > scrollHeight * 0.9) {
        this.getNextData();
      }
    }
  };

  renderResults = () => {
    const { getData } = this.context;
    const { results, status } = getData(Search.defaultData);

    if (status === 'success' || status === 'updating') {
      return (
        <CardColumns className="CardColumns">
          {results.map(item => (
            <Card key={item.id}>
              <CardBody>
                <CardTitle>{item.title}</CardTitle>
                <CardSubtitle>{item.updated_date}</CardSubtitle>
                <ReactMarkdown source={item.body} />
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.url}
                </a>
                {/* <ReactPlayer url='https://www.youtube.com/watch?v=ysz5S6PUM-U' width='480' /> */}
              </CardBody>
            </Card>
          ))}
          {status === 'updating' && (
            <div className="search_updating">
              <ReactLoading
                type="spin"
                color={Colors.GRAY3}
                height={50}
                width={50}
              />
            </div>
          )}
        </CardColumns>
      );
    } else if (status === 'error') {
      return <div>The request did not succeed.</div>;
    } else if (status === 'loading') {
      return (
        <div className="search_loading">
          <ReactLoading
            type="spin"
            color={Colors.GRAY3}
            height={100}
            width={100}
          />
        </div>
      );
    }
  };

  componentDidMount() {
    const { getData } = this.context;
    const data = getData(Search.defaultData);
    if (data.status === null) {
      this.getFirstData();
    }
  }

  componentDidUpdate() {
    const { getParam, getData } = this.context;
    const { search: lastSearch } = getData(Search.defaultData);
    const search = getParam('search');
    if (search !== lastSearch) {
      this.getFirstData();
    }
  }

  render() {
    const { getParam } = this.context;
    const search = getParam('search');

    return (
      <div className="search widget">
        <Navbar color="light" light expand="md" className="search_navbar">
          <InputGroup>
            <Input
              onChange={this.handleChangeSearch}
              defaultValue={search}
              placeholder="Search..."
            />
          </InputGroup>
        </Navbar>
        <div
          className="search_results"
          onScroll={this.handleScroll}
          ref={this.resultsEl}
        >
          {this.renderResults()}
        </div>
      </div>
    );
  }
}

export default Search;
