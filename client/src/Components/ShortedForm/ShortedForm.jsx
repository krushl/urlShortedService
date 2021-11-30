import React, {useState, useEffect} from 'react'
import short from "./ShortedForm.module.css";


const ShortedForm = () => {
    const [data, setData] = useState({})
    const requestOptions = {
        method: 'POST',
        headers: {'Content-type': 'application/json'},
        body: JSON.stringify({data})
    }

    function handleClick(e) {
        e.preventDefault()
        fetch("/test", requestOptions)
            .then(response => {
                    if (response.status === 200) {
                        alert("JOPA")
                    } else {
                        alert("neJOPA")
                    }
                }
            )
        console.log(data)

    }

    function handleChange(e) {
        let name = e.target.name

        data[name]=e.target.value

        setData({...data})
    }

    return (
        <div className={short.container}>
            <form method="POST" >
                <div className={short.formContainer}>
                <div>
                    <input className={short.input} type="text" name="url" onChange={handleChange} placeholder="Вставьте ссылку" required/>
                </div>
                <div>
                    <input className={short.input} type="text" name="alias_url" onChange={handleChange} placeholder="Псевдоним"/>
                </div>
                <div>
                    <select className={short.input} name="type_id"  value={data['type_id']} onChange={handleChange}>
                        <option value='1'>public</option>
                        <option value='2'>private</option>
                        <option value='3'>authorized</option>
                    </select>
                </div>
                <div>
                    <input className={short.input} type="submit" value="Отправить" onClick={handleClick}/>
                </div>
                </div>
            </form>
        </div>


    );
}

export default ShortedForm;