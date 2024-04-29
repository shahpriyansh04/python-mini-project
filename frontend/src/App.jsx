import { useState } from 'react';

function App() {

  const [input,setInput] = useState();
  const [movies,setMovies] = useState([]);
  const handleClick = async () => {
    const res = await fetch(`http://localhost:5000/?movie=${input}`)
    const data = await res.json();
    setMovies(data);
  }

  return (
   <div className=' h-screen w-screen bg-gray-900 flex flex-col items-center py-20'>
    <input className=' px-3 py-4 outline-none' type='text' value={input} onChange={(e) => {setInput(e.target.value)}}  placeholder='Enter a movie name'/>
<button className='mt-12 bg-white px-12 py-4' onClick={handleClick}>Search</button>
{
  movies.length > 0 ? (
    <div className='grid h-full grid-cols-6 gap-12 mt-12'>
    {movies.map((movie) => (
      <div className="h-72 text-white flex flex-col items-center ">
        <img src={movie.poster} alt={movie.name} className='w-full h-full object-contain' />
        <h2>{movie.name}</h2>
      </div>
    ))}
    </div>
  ) : (
    <div className='text-white mt-12'>No movies available</div>
  )
}

   </div>
  )
}

export default App
