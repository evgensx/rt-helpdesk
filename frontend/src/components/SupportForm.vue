<script setup lang="ts">
import {
  submitForm,
  formData,
  formatPhoneNumber,
  formIsValid,
  isTrue,
} from "@/ts/formScripts";
</script>

<template>
  <div v v-if="isTrue">
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
