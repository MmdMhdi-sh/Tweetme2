import React, {useEffect, useState} from "react";

import { Tweet } from "./detail";
import { apiTweetList } from "./lookup";


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
            apiTweetList(props.username, handleTweetListLookup)
        }
    }, [tweetsInit, tweetsDidSet, setTweetsDidSet, props.username])
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