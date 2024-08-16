import React, {useEffect, useState} from "react";
import { 
    apiTweetAction,
    apiTweetCreate,  
    apiTweetList 
} from "./lookup";

  
export function TweetsComponent(props) {
    console.log("props = ", props)
    const textAreaRef = React.createRef()
    const [newTweets, setNewTweets] = useState([])
    // backend api response handler
    const handleBackendUpdate = (response, status) => {
        let tempNewTweets = [...newTweets]
        if (status === 201) {
            tempNewTweets.unshift(response)
            setNewTweets(tempNewTweets)
        } else {
            console.log(response)
            alert("An error occured. Please try again.")
        }
    }
    // backend api request handler
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        apiTweetCreate(newVal, handleBackendUpdate)
        textAreaRef.current.value = ''
    }
    return <div className={props.className}>
        <div className="col-12 mb-3">
            <form onSubmit={handleSubmit} name="tweet"> 
                <textarea ref={textAreaRef} required={true} className="form-control"></textarea>
                <button type="submit" className="btn btn-primary my-3">Tweet</button>
            </form>
        </div>
        <TweetsList newTweets={newTweets} />
    </div>
}

export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    // setTweetsInit([...props.newTweets].concat(tweetsInit))
    useEffect(()=>{
        const final = [...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length) {
            setTweets(final)
        }  
    }, [props.newTweets, tweets, tweetsInit])
    useEffect(() => {
        if (tweetsDidSet === false) {
            const handleTweetListLookup = (response, status) => {
                if (status === 200){
                    setTweetsInit(response)
                    setTweetsDidSet(true)
                } else {
                    alert("There was an error!")
                }
            }
            apiTweetList(handleTweetListLookup)
        }
    }, [tweetsInit, tweetsDidSet, setTweetsDidSet])
    const handleDidRetweet = (newTweet) => {
        const updateTweetsInit = [...tweetsInit]
        updateTweetsInit.unshift(newTweet)
        setTweetsInit(updateTweetsInit)
        const updateFinalTweets = [...tweets]
        updateFinalTweets.unshift(newTweet)
        setTweets(updateFinalTweets)
    }
    return tweets.map((item, index)=>{
      return <Tweet 
        tweet={item} 
        didRetweet={handleDidRetweet}
        key={`${index}-{item.id}`} 
        className='my-5 py-5 border bg-white text-dark' />
    })
}


export function ActionBtn(props) {
    const {tweet, action, didPerformAction} = props
    const likes = tweet.likes ? tweet.likes : 0
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    const handleActionBackendEvent = (response, status) => {
        console.log(status, response)
        if ((status === 200 || status === 201) && didPerformAction) {
            didPerformAction(response, status)
        }
    }
    const handleClick = (event) => {
        event.preventDefault()
        apiTweetAction(tweet.id, action.type, handleActionBackendEvent)
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
}
  
export function ParentTweet(props) {
    const {tweet} = props 
    return tweet.parent ? <div className='row'>
        <div className='col-11 mx-auto p-3 border rounded'>
            <p className='mb-0 text-muted small'>Retweet</p>
            <Tweet hideActions className={' '} tweet={tweet.parent} />
        </div>
    </div> : null
}

export function Tweet(props) {
    const {tweet, didRetweet, hideActions} = props
    // before the below hook and related changes, it was needed to reload the page to see action changes.
    const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null)
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    const handlePerformAction = (newActionTweet, status) => {
        if (status === 200) {
            setActionTweet(newActionTweet)
        } else if (status === 201) {
            //  let the tweet list know
            if (didRetweet) {
                didRetweet(newActionTweet)
            }
        }
    }

    return <div className={className}>
        <div>
            <p>{tweet.id} - {tweet.content}</p>
            <ParentTweet tweet={tweet} />
        </div>
      
      {(actionTweet && hideActions !== true) && <div className='btn btn-group'>
        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'like', display:'Likes'}} />
        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'unlike', display:'Unlike'}} />
        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{type:'retweet', display:'Retweet'}} />
      </div>}
    </div>
}