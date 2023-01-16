<script setup lang="ts">
import { ref, computed } from "vue";
// import type { Ref } from "vue";

const formData = ref({
  lastName: "Иванов",
  firstName: "Иван",
  patronymicName: "Иванович",
  tel: "+7 (123) 456 78 90", //+7 (123) 456 78 90
  textarea: "помогите",
});

// inferred type: ComputedRef<number>
const formattedPhoneNumber = computed(() => {
  return formData.value.tel.replace(
    /(\+\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/g,
    "$1 ($2) $3 $4 $5"
  );
});

const formIsValid = computed(() => {
  return (
    formData.value.lastName.trim() !== "" &&
    formData.value.firstName.trim() !== "" &&
    formData.value.patronymicName.trim() !== "" &&
    formData.value.tel.trim() !== "" &&
    formData.value.textarea.trim() !== ""
  );
});

//Replace value in form object
let formatPhoneNumber = () => {
  formData.value.tel = formattedPhoneNumber.value;
};

// Fetch request to backend server
const submitForm = async () => {
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
</script>

<template>
  <div>
    <h2>Заполните поля формы ниже</h2>
  </div>
  <div id="container">
    <form @submit.prevent="submitForm" name="request" autocomplete="off">
      <div class="field">
        <label class="field-label" for="post-last">
          <span class="star-red">*</span> Фамилия
        </label>
        <input
          v-model="formData.lastName"
          class="field-input"
          id="post-last"
          type="text"
          name="last_name"
          placeholder="Фамилия"
          autocomplete="family-name"
          required
          autofocus
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-first">
          <span class="star-red">*</span> Имя
        </label>
        <input
          v-model="formData.firstName"
          class="field-input"
          type="text"
          name="first_name"
          id="post-first"
          placeholder="Имя"
          autocomplete="name"
          required
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-father">
          <span class="star-red">*</span> Отчество
        </label>
        <input
          v-model="formData.patronymicName"
          class="field-input"
          type="text"
          name="patronymic_name"
          id="post-father"
          placeholder="Отчество"
          autocomplete="given-name"
          required
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-tel">
          <span class="star-red">*</span> Телефон
        </label>
        <input
          v-model="formData.tel"
          @focus.once="formData.tel = '+7'"
          @input="formatPhoneNumber"
          class="field-input"
          type="tel"
          name="tel"
          id="post-tel"
          placeholder="+7"
          autocomplete="tel"
          pattern="\+7 \([0-9]{3}\) [0-9]{3} [0-9]{2} [0-9]{2}"
          maxlength="18"
          required
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-request">
          <span class="star-red">*</span> Обращение
        </label>
        <textarea
          v-model="formData.textarea"
          class="field-input"
          name="request_text"
          id="post-request"
          placeholder="Введите текст обращения"
          required
          rows="3"
          autocomplete="off"
        ></textarea>
      </div>
      <div class="field">
        <button
          :disabled="!formIsValid"
          class="field__button"
          type="submit"
          target="_self"
        >
          Отправить
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts"></script>

<style scoped>
input {
  height: 30px;
}

.field {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  padding-top: 5px;
}

.field-label {
  font-size: 0.96em;
  margin-right: 5px;
}

.star-red {
  color: #ff0000;
}

.field-input {
  min-width: 60%;
  width: 200px;
}

.field__button {
  /* align-self: flex-start; */
  margin-right: 40%;
}

textarea {
  resize: vertical;
}

@media (max-width: 362px) {
  .field {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .field__button {
    margin: auto;
  }
}
</style>

<!-- <script lang="ts">
const API_URI = "http://" + document.location.hostname + ":8080/submit";
console.log(API_URI);
var submitButton = document.getElementsByClassName("button-sent")[0];
var form = document.forms.request;

async function asyncJson() {
  let object = {};
  let formData = new FormData(form);
  formData.forEach((value, key) => (object[key] = value));

  let response = await fetch(API_URI, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json; charset=UTF-8",
    },
    body: JSON.stringify(object),
  });
  if (response.ok) {
    var formContainer = document.getElementsByClassName("form-container")[0];
    formContainer.setAttribute(
      "style",
      "justify-content: center; align-items: center"
    );
    formContainer.innerHTML = "<h2>Спасибо за обращение!</h2>";
    return response.json();
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
  return;
}

submitButton.addEventListener("click", (event) => {
  if (form.checkValidity()) {
    event.preventDefault();
    asyncJson();
  }
});
</script> -->
