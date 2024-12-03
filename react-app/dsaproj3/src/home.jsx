import React, { useState, useEffect } from 'react'
import './index.css';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

function CircularIndeterminate() {
  return (
    <Box sx={{ display: 'flex' }}>
      <CircularProgress />
    </Box>
  );
}

const HomePage = () => {

  const [flowState, setFlowState] = useState(0);
  const [requestData, setRequestData] = useState({});
  const [error, setError] = useState('');

  /**
   * {
   *  request_type: tf-idf or iis
   *  param: player_name
   *  value: curry
   *  result_limit: 10
   * }
   */

  const [algorithmSelectorOpen, setAlgorithmSelectorOpen] = useState(false);
  const [algorithmSelected, setAlgorithmSelected] = useState('');

  const [queryByOpen, setQueryByOpen] = useState(false);
  const [queryBySelected, setQueryBySelected] = useState('');
  const [query, setQuery] = useState('');

  const [searchResultsCountInput, setSearchResultsCountInput] = useState(0);

  const [requestLoading, setRequestLoading] = useState(false);

  return (
    <div className="flex flex-col w-full min-h-screen items-center justify-center bg-black">
      <h1 className="text-4xl font-bold text-white">Welcome to the NBA Shot Search Engine</h1>

      {
        flowState === 0 && (
          <div className="flex flex-col items-center justify-center w-full h-">
              <p className="text-xl mt-12 font-regular text-white">Let's start with how you want to search.</p>

              <button 
              onClick={() => setAlgorithmSelectorOpen(!algorithmSelectorOpen)}
              className="relative flex flex-row space-x-0 items-center w-[12.5rem] justify-center text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark hover:bg-hovernewdark font-bold text-lg">
                <span>{
                  algorithmSelected === '' ? 'Select Algorithm' : algorithmSelected
                } </span>
                <ArrowDropDownIcon
                      sx={{
                      fontSize: 24,
                      color: 'white',
                      transform: algorithmSelectorOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                      }}
                  />

                  {
                    algorithmSelectorOpen && (
                      <div className="absolute top-10 left-0 w-[12.5rem] z-10 bg-secondarynewdark border border-1 border-neutral-700 p-4 rounded-xl mt-2">
                        <button onClick={() => {
                          setAlgorithmSelected('TF-IDF');
                          setAlgorithmSelectorOpen(false);
                        }} className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">TF-IDF</button>
                        <button onClick={() => {
                          setAlgorithmSelected('IIS');
                          setAlgorithmSelectorOpen(false);
                        }} className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">IIS</button>
                      </div>
                    )
                  }
              </button>

              {
                algorithmSelected !== '' && (
                  <button
                  onClick={() => {
                    if(algorithmSelected === '') {
                      setError('Please select an algorithm');
                    } else {
                      setFlowState(1);
                    }
                  }}
                  className="flex flex-row space-x-2 items-center justify-center text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark hover:bg-hovernewdark font-bold text-lg">
                    <span>Next</span>
                  </button>
                )
              }
          </div>
        )
      }

      {
        flowState === 1 && (
          <div className="flex flex-col items-center justify-center w-full h-">
              <p className="text-xl mt-12 font-regular text-white">Now, choose what you want to query by.</p>

              <button 
              onClick={() => setQueryByOpen(!queryByOpen)}
              className="relative flex flex-row space-x-0 items-center w-[12.5rem] justify-center text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark hover:bg-hovernewdark font-bold text-lg">
                <span>{
                  queryBySelected === '' ? 'Select Query' : (
                    queryBySelected === 'player_name' ? 'Player Name' :
                    queryBySelected === 'event_type' ? 'Event Type' :
                    queryBySelected === 'shot_type' ? 'Shot Type' :
                    queryBySelected === 'basic_zone' ? 'Basic Zone' :
                    queryBySelected === 'zone_name' ? 'Zone Name' :
                    queryBySelected === 'action_type' ? 'Action Type' : ''
                  )
                } </span>
                <ArrowDropDownIcon
                      sx={{
                      fontSize: 24,
                      color: 'white',
                      transform: queryByOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                      }}
                  />

                  {
                    queryByOpen && (
                      <div className="absolute top-10 left-0 w-[12.5rem] z-10 bg-secondarynewdark border border-1 border-neutral-700 p-4 rounded-xl mt-2">
                        <button onClick={() => {
                          setQueryBySelected('player_name');
                          setQueryByOpen(false);
                        }} className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">Player Name</button>
                        <button onClick={() => {
                          setQueryBySelected('event_type');
                          setQueryByOpen(false);
                        }} className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">Event Type</button>
                        <button onClick={() => {
                          setQueryBySelected('shot_type');
                          setQueryByOpen(false);
                        }
                        } className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">Shot Type</button>
                        <button onClick={() => {
                          setQueryBySelected('basic_zone');
                          setQueryByOpen(false);
                        }} className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">Basic Zone</button>
                        <button onClick={() => {
                          setQueryBySelected('zone_name');
                          setQueryByOpen(false);
                        }} className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">Zone Name</button>
                        <button onClick={() => {
                          setQueryBySelected('action_type');
                          setQueryByOpen(false);
                        }} className="w-full text-left hover:bg-hovernewdark px-4 py-2 rounded-lg">Action Type</button>
                      </div>
                    )
                  }
              </button>

              {
                queryBySelected !== '' && (
                  <input 
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter query"
                  className="w-[12.5rem] text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark font-bold text-lg ring-0 outline-none active:ring-0"/>
                )
              }

              {
                queryBySelected !== '' && (
                  <button
                  onClick={() => {
                    if(queryBySelected === '') {
                      setError('Please select a query option');
                    } else {
                      if(query === '') {
                        setError('Please enter a query');
                      } else {
                        setFlowState(2);
                      }
                    }
                  }}
                  className="flex flex-row space-x-2 items-center justify-center text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark hover:bg-hovernewdark font-bold text-lg">
                    <span>Next</span>
                  </button>
                )
              }

              {
                queryBySelected !== '' && (
                  <h1 className="text-3xl mt-12 font-bold text-white">Instructions</h1>
                )
              }
              {
                queryBySelected === 'player_name' && (
                  <div className="flex flex-col space-y-2">
                    <p className="text-xl font-regular text-white">Enter the player name you want to search for.</p>
                  </div>
                )
              }
              {
                queryBySelected === 'event_type' && (
                  <div className="flex flex-col space-y-2">
                    <p className="text-center text-xl font-regular text-white">Enter either "Made Shot" or "Missed Shot".</p>
                  </div>
                )
              }
              {
                queryBySelected === 'shot_type' && (
                  <div className="flex flex-col space-y-2">
                    <p className="text-center text-xl font-regular text-white">Enter either "2PT Field Goal" or "3PT Field Goal".</p>
                  </div>
                )
              }
              {
                queryBySelected === 'basic_zone' && (
                  <div className="flex flex-col space-y-2 max-w-screen-md">
                    <p className="text-center text-xl font-regular text-white">Enter Restricted Area, In the Paint (non-RA), Midrange, Left Corner 3, Right Corner 3, Above the Break, or Backcourt.</p>
                  </div>
                )
              }
              {
                queryBySelected === 'zone_name' && (
                  <div className="flex flex-col space-y-2 max-w-screen-md">
                    <p className="text-center text-xl font-regular text-white">Enter left, left side center, center, right side center, or right</p>
                  </div>
                )
              }
              {
                queryBySelected === 'action_type' && (
                  <div className="flex flex-col space-y-2 max-w-screen-md">
                    <p className="text-center text-xl font-regular text-white">Enter the description of shot type (layup, dunk, jump shot, etc.)</p>
                  </div>
                )
              }
          </div>
        )
      }

      {
        flowState === 2 && (
          <div className="flex flex-col items-center justify-center w-full h-">
              <p className="text-xl mt-12 font-regular text-white">Now, enter the number of search results you want to see.</p>

              <input 
              value={searchResultsCountInput}
              onChange={(e) => setSearchResultsCountInput(e.target.value)}
              placeholder="Enter number of results"
              className="w-[12.5rem] text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark font-bold text-lg ring-0 outline-none active:ring-0"/>

              {
                searchResultsCountInput !== 0 && (
                  <button
                  onClick={() => {
                    if(searchResultsCountInput === 0) {
                      setError('Please enter a number of results');
                    } else {
                      setFlowState(3);
                    }
                  }}
                  className="flex flex-row space-x-2 items-center justify-center text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark hover:bg-hovernewdark font-bold text-lg">
                    <span>Next</span>
                  </button>
                )
              }
          </div>
        )
      }

      {
        flowState === 3 && (
          <div className="flex flex-col items-center justify-center w-full h-">
              <p className="text-xl mt-12 font-regular text-white">Now, click the button below to search.</p>

              { requestLoading ? (
                <div className="mt-4">
                  <CircularIndeterminate /> 
                </div>
              ) : (
                <button
                onClick={() => {
                  setRequestLoading(true);
                  fetch('http://127.0.0.1:5000/api/query', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    // credentials: 'include',
                    credentials: 'include',
                    body: JSON.stringify({
                      request_type: (algorithmSelected === 'TF-IDF' ? 'tfidf' : 'iis'),
                      param: queryBySelected,
                      value: query,
                      result_limit: searchResultsCountInput
                    })
                  })
                  .then(response => response.json())
                  .then(data => {
                    setRequestLoading(false);
                    setRequestData(data);
                    setFlowState(4);
                  })
                  .catch(err => {
                    setError('An error occurred. Please try again.');
                  })
                }}
                className="flex flex-row space-x-2 items-center justify-center text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark hover:bg-hovernewdark font-bold text-lg">
                  <span>Search</span>
                </button>
              )}

          </div>
        )
      }

      {
        flowState === 4 && (
          <div className="flex flex-col items-center justify-center w-full h-auto">
              <p className="text-xl mt-12 mb-4 font-regular text-white">The query took {requestData.time} seconds and {requestData.count} results were found.</p>

              <div className="flex flex-col space-y-4 max-w-screen-lg  w-full h-[36rem] overflow-y-scroll">
                {
                  requestData?.results?.length > 0 && requestData?.results?.map((result, index) => (
                    <div key={index} className="flex flex-col mt- rounded-xl bg-secondarynewdark px-6 py-6  w-full h-">
                      <p className="text-3xl text-left font-bold text-white">Result {index + 1} • {result.player_name}</p>
                      <p className="text-xl mt-3 font-regular text-white">{
                        result.event_type === 'Made Shot' ? (<span className="text-green-500">Made Shot</span>) : (<span className="text-red-500">Missed Shot</span>)
                        } • {result.shot_type}</p>
                      <p className="text-xl mt- font-regular text-white">Basic Zone: {result.basic_zone} • {result.zone_name}</p>
                      <p className="text-lg mt- font-regular text-white">{result.action_type}</p>
                    </div>
                  ))
                }
              </div>

              <button 
              onClick={() => {
                setFlowState(0);
                setAlgorithmSelected('');
                setQueryBySelected('');
                setQuery('');
                setSearchResultsCountInput(0);
                setError('');
              }}
              className="flex flex-row space-x-2 items-center justify-center text-white px-4 py-2 rounded-xl mt-2 bg-secondarynewdark hover:bg-hovernewdark font-bold text-lg"
              >
                Search Again
              </button>
          </div>
        )
      }

      {
        error !== '' && (
          <p className="text-red-500 mt-2">{error}</p>
        )
      }
    </div>
  );
}

export default HomePage