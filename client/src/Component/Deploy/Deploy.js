 import React, { useState, useEffect } from 'react' 

export const Deploy = () => {
    const [data, setData] = useState([{}])

    useEffect(() => {
    fetch("/members").then(
        res => res.json()
    ).then(
        data => {
        setData(data)
        console.log(data)
       }
    )
    }, [])

    return (
    <div>
        
    {(typeof data.members === 'undefined') ? (
        <p>Loading...</p>
    ) : (
        data.members.map((member,i) => (
        <p key={i}>{member}</p>
        ))
    )}

    </div>
    )
}