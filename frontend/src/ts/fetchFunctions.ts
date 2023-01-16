export async function fetchData(formData: {
  tel: string;
  lastName: string;
  firstName: string;
  patronymicName: string;
  textarea: string;
}) {
  try {
    const inTel: string = formData.tel;
    const outTel = inTel.replace(/[^0-9]/g, "");
    const origin = window.location.origin;
    const data = {
      last_name: formData.lastName,
      first_name: formData.firstName,
      patronymic_name: formData.patronymicName,
      tel: outTel,
      request_text: formData.textarea,
    };
    console.log(formData);
    const response = await fetch(origin + ":8888/submit", {
      method: "POST",
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    });
    const json = await response.json();
    // Do something with the data
    console.log(json);
    return json;
  } catch (error) {
    // Handle the error
    console.error(error);
  }
}
