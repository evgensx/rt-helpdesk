<script setup lang="ts">
import { ref } from "vue";
const counter = ref(0);
</script>

<template>
  <div class="container">
    <form @submit.prevent="counter++" name="request" autocomplete="off">
      <div class="field">
        <label class="field-label" for="post-last">
          <span class="star-red">*</span> Фамилия
        </label>
        <input
          class="field-input"
          id="post-last"
          type="text"
          name="last_name"
          placeholder="Фамилия"
          autocomplete="family-name"
          required
          autofocus
          value="Ivanov"
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-first">
          <span class="star-red">*</span> Имя
        </label>
        <input
          class="field-input"
          type="text"
          name="first_name"
          id="post-first"
          placeholder="Имя"
          autocomplete="name"
          required
          value="Ivan"
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-father">
          <span class="star-red">*</span> Отчество
        </label>
        <input
          class="field-input"
          type="text"
          name="patronymic_name"
          id="post-father"
          placeholder="Отчество"
          autocomplete="given-name"
          required
          value="Ivanovich"
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-tel">
          <span class="star-red">*</span> Телефон
        </label>
        <input
          class="field-input"
          type="tel"
          name="tel"
          id="post-tel"
          placeholder="+7"
          autocomplete="tel"
          pattern="\+7[0-9]{3}[0-9]{3}[0-9]{2}[0-9]{2}"
          required
          value="+71234567890"
        />
      </div>
      <div class="field">
        <label class="field-label" for="post-request">
          <span class="star-red">*</span> Обращение
        </label>
        <textarea
          class="field-input"
          name="request_text"
          id="post-request"
          placeholder="Введите текст обращения"
          required
          autocomplete="off"
          v-model="counter"
        ></textarea>
      </div>
      <div class="field">
        <div></div>
        <div class="button-field">
          <button class="button-sent" role="button" target="_self">
            Отправить
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
export default {
  name: "post-request-async-await",
  data() {
    return {
      postId: null,
    };
  },
  async created() {
    // POST request using fetch with async/await
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title: "Vue POST Request Example" }),
    };
    const response = await fetch(
      "https://jsonplaceholder.typicode.com/posts",
      requestOptions
    );
    const data = await response.json();
    this.postId = data.id;
  },
};
</script>

<style scoped>
.container {
  display: flex;
}

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
  font-size: smaller;
  margin-right: 5px;
}

.star-red {
  color: #ff0000;
}

.field-input {
  min-width: 60%;
  width: 200px;
}

div .button-field {
  min-width: 60%;
  width: 200px;
}

textarea {
  height: 60px;
}

@media (max-width: 362px) {
  .field {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  div .button-field {
    display: flex;
    justify-content: center;
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
