import { useState } from 'react';

const TextInputForm = () => {
  const [input, setInput] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Submit logic goes here
    console.log(input);
  };

  return (
    <div className="flex flex-col w-full gap-2">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2 w-[40%] m-10 relative">
        <textarea
          className="w-full h-40 px-5 py-3 pb-10 outline-none resize-none rounded-3xl shadow-lg"
          placeholder="文章を入力して下さい"
          value={input}
          onChange={(e) => setInput(e.target.value)} 
        />
        <button
          type="submit"
          className={`absolute right-0 bottom-4 mb-1 mr-4 w-10 h-10 rounded-full flex items-center justify-center ${input ? "bg-slate-700" : "bg-gray-400 cursor-not-allowed"}`}
          disabled={!input}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6 text-white" viewBox="0 0 24 24">
            <path fill="currentColor" d="M3 20V4l19 8M5 17l11.85-5L5 7v3.5l6 1.5l-6 1.5M5 17V7v6.5Z" />
          </svg>
        </button>
      </form>
    </div>
  );
};

export default TextInputForm;
