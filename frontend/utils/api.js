const API_URL =
  process.env
  .NEXT_PUBLIC_API_URL;


/*
---------------------------------
UPLOAD DOCUMENT
---------------------------------
*/

export async function uploadDocument(
  file
){

  const formData =
    new FormData();

  formData.append(
    "file",
    file
  );

  const response =
    await fetch(

      `${API_URL}/upload`,

      {
        method:"POST",
        body:formData
      }

    );

  if(!response.ok){

    throw new Error(
      "Upload failed"
    );

  }

  return response.json();
}


/*
---------------------------------
FETCH ANALYSIS HISTORY
---------------------------------
*/

export async function fetchAnalyses(){

  const response =
    await fetch(

      `${API_URL}/analyses`

    );

  if(!response.ok){

    throw new Error(
      "Fetch analyses failed"
    );

  }

  return response.json();
}


/*
---------------------------------
CHAT WITH CONTRACT
---------------------------------
*/

export async function askContract(

  contractId,

  question

){

  const response =
    await fetch(

      `${API_URL}/chat`,

      {

        method:"POST",

        headers:{
          "Content-Type":
          "application/json"
        },

        body:JSON.stringify({

          contract_id:
          Number(contractId),

          question

        })

      }

    );

  const data =
    await response.json();
 console.log(
    "CHAT RESPONSE:",
    data
  );
  if(!response.ok){

    console.error(
      "BACKEND ERROR:",
      data
    );

    throw new Error(

      data.error ||

      "Chat failed"

    );

  }

  return data;

}