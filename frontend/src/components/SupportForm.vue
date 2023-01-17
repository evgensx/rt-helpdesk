<script setup lang="ts">
import { ref, computed } from "vue";
import {
  submitForm,
  formData,
  formatPhoneNumber,
  formIsValid,
  isTrue,
  // formChecker,
} from "@/ts/formScripts";

const checker = ref(() => {
  // if (formIsValid) {

  // }
  return true;
});

// let count = ref(0);

const textLength = computed(() => formData.value.textarea.length);
</script>

<template>
  <div v-if="isTrue">
    <h2>
      Данные приняты<br />
      Спасибо за обращение
    </h2>
  </div>
  <div v-else>
    <div>
      <h2>Заполните поля формы ниже</h2>
    </div>
    <form @submit.prevent="submitForm" name="request" autocomplete="off">
      <div class="field">
        <label class="field-label" for="post-last">
          <span class="star-red">*</span> Фамилия
        </label>
        <input
          v-model="formData.lastName"
          v-on:keyup="checker"
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
      <div v-if="d"></div>
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
          autocomplete="given-name"
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
          autocomplete="additional-name"
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
          minlength="18"
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
          maxlength="280"
          minlength="8"
          v-bind:rows="3"
          v-on:keyup="1"
          autocomplete="off"
        ></textarea>
      </div>
      <div class="valid">{{ textLength }} / 280</div>
      <div class="field">
        <button
          v-bind:disabled="formIsValid"
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
  /* top|right|down|left */
  margin: 3px 40%;
  padding: 4px 6px;
}

textarea {
  resize: vertical;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue",
    sans-serif;
  padding: 4px;
}
.valid {
  margin-right: 0px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  font-size: 0.8em;
}

@media (max-width: 362px) {
  .field {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .field__button {
    margin: 5px auto;
  }
}
</style>
