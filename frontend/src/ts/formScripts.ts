import { ref, computed, reactive } from "vue";

export const formData = ref({
  lastName: "",
  firstName: "",
  patronymicName: "",
  tel: "",
  textarea: "",
});

// inferred type: ComputedRef<number>
const formattedPhoneNumber = computed(() => {
  return formData.value.tel.replace(
    /(\+\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/g,
    "$1 ($2) $3 $4 $5"
  );
});

export const formIsValid = computed(() => {
  return (
    formData.value.lastName.trim() !== "" &&
    formData.value.firstName.trim() !== "" &&
    formData.value.patronymicName.trim() !== "" &&
    formData.value.tel.trim() !== "" &&
    formData.value.textarea.trim() !== "" &&
    /\+7 \([0-9]{3}\) [0-9]{3} [0-9]{2} [0-9]{2}/.test(
      formData.value.tel.trim()
    )
  );
});

//Replace value in form object
export const formatPhoneNumber = () => {
  formData.value.tel = formattedPhoneNumber.value;
};

// function formChecker() {
//   if (formIsValid.value) {
//   }
// }

// Define var
export const isTrue = ref(false);

// Fetch request to backend server
export const submitForm = async () => {
  try {
    const data = {
      last_name: formData.value.lastName,
      first_name: formData.value.firstName,
      patronymic_name: formData.value.patronymicName,
      tel: formData.value.tel,
      request_text: formData.value.textarea,
    };
    const res = await fetch(
      "http://" + window.location.hostname + ":8888/submit",
      {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (res.ok) {
      isTrue.value = true;
      const json = await res.json();
      // Do something with the response data
      console.log(json);
    } else {
      // handle the error
    }
  } catch (error) {
    // Handle the error
    console.error(error);
  }
};
