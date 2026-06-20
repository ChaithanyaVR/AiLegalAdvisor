'use client';

import {
  useState
} from "react";

import {
  askContract
} from "../../../utils/api";

export default function ContractChat({

  contractId

}){

  const [

    question,

    setQuestion

  ] = useState("");

  const [

    answer,

    setAnswer

  ] = useState("");

  const [

    loading,

    setLoading

  ] = useState(false);

  async function handleAsk(){

    if(!question){

      return;

    }

    try{

      setLoading(
        true
      );

      const data =
        await askContract(

          contractId,

          question

        );

      setAnswer(
        data.answer
      );

    }catch(err){

      console.error(
        err
      );

    }finally{

      setLoading(
        false
      );

    }

  }

  return(

    <div className="
      mt-8
      bg-zinc-900
      border
      border-zinc-800
      rounded-xl
      p-6
    ">

      <h2 className="
        text-xl
        font-bold
        mb-4
      ">
        Chat With Contract
      </h2>

      <input

        type="text"

        value={question}

        onChange={(e)=>

          setQuestion(
            e.target.value
          )

        }

        placeholder="
          Ask about this contract...
        "

        className="
          w-full
          p-3
          rounded-lg
          bg-zinc-950
          border
          border-zinc-700
          mb-4
        "

      />

      <button

        onClick={
          handleAsk
        }

        className="
          w-full
          bg-blue-600
          hover:bg-blue-700
          py-3
          rounded-lg
          font-semibold
        "

      >

        {

          loading

          ?

          "Thinking..."

          :

          "Ask"

        }

      </button>

      {

        answer && (

          <div className="
            mt-6
            bg-zinc-950
            p-4
            rounded-lg
          ">

            <h3 className="
              font-bold
              mb-2
            ">
              Answer
            </h3>

            <p className="
              text-zinc-300
              whitespace-pre-wrap
            ">

              {answer}

            </p>

          </div>

        )

      }

    </div>

  );

}


