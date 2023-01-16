import { ref, computed } from "vue";

export const formData = ref({
  lastName: "Иванов",
  firstName: "Иван",
  patronymicName: "Иванович",
  tel: "+7 (123) 456 78 90", //+7 (123) 456 78 90
  textarea: "помогите",
});

// inferred type: ComputedRef<number>
export const formattedPhoneNumber = computed(() => {
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
    formData.value.textarea.trim() !== ""
  );
});

//Replace value in form object
export const formatPhoneNumber = () => {
  formData.value.tel = formattedPhoneNumber.value;
};

// Define var
export let isTrue = false;

// Fetch request to backend server
export const submitForm = async () => {
  try {
    const res = await fetch(
      "http://" + window.location.hostname + ":8888/submit",
      {
        method: "POST",
        body: JSON.stringify(formData.value),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (res.ok) {
      isTrue = true;
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
