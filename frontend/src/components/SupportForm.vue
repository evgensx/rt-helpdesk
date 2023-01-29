<template>
  <div v-if="isTrue" class="box" id="all-right">
    <h2>
      Данные приняты<br />
      Спасибо за обращение
    </h2>
    <button v-on:click="routeBack" class="field__button" id="back">Назад</button>
  </div>
  <div v-else>
    <div class="head">
      <h3>Заполните поля формы ниже</h3>
    </div>
    <div class="box">
      <form @submit.prevent="submitForm" name="request" autocomplete="off">
        <div class="field">
          <label class="field-label" for="post-last">
            <span class="star-red">*</span> Фамилия
          </label>
          <input
            v-model="formData.lastName"
            class="field__input"
            id="post-last"
            type="text"
            name="last_name"
            placeholder="Фамилия"
            autocomplete="family-name"
            v-bind:pattern="patternValue"
            maxlength="25"
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
            class="field__input"
            type="text"
            name="first_name"
            id="post-first"
            placeholder="Имя"
            autocomplete="given-name"
            v-bind:pattern="patternValue"
            maxlength="25"
            required
          />
        </div>
        <div class="field">
          <label class="field-label" for="post-father">
            <span class="star-red">*</span> Отчество
          </label>
          <input
            v-model="formData.patronymicName"
            class="field__input"
            type="text"
            name="patronymic_name"
            id="post-father"
            placeholder="Отчество"
            maxlength="25"
            v-bind:pattern="patternValue"
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
            class="field__input"
            type="tel"
            name="tel"
            id="post-tel"
            placeholder="+7"
            autocomplete="tel"
            v-bind:pattern="patternPhone"
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
            class="field__input"
            name="request_text"
            id="post-request"
            placeholder="Введите текст обращения"
            required
            maxlength="280"
            minlength="8"
            :rows="rowCount"
            v-on:input="rowCounter"
            spellcheck="true"
            autocomplete="off"
          ></textarea>
        </div>
        <!-- <div class="clone">{{ formData.textarea }}</div> -->
        <div class="valid">{{rowCounted}} | {{ rowCount }} | {{ textLength }} / 280</div>
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
  </div>
</template>

<script lang="ts">
import { ref, computed } from "vue";
import {
  submitForm,
  formData,
  formatPhoneNumber,
  formIsValid,
  isTrue,
  // formChecker,
} from "@/ts/formScripts";

export default {
  setup() {
    const patternValue = "[A-Za-zА-Яа-яЁё\\s-]{2,}";
    const patternPhone = "\\+7 \\([0-9]{3}\\) [0-9]{3} [0-9]{2} [0-9]{2}";

    // const checker = ref(() => {
    //   // if (formIsValid) {

    //   // }
    //   return true;
    // });
    const rowCount = ref(2);

    const rowCounted = computed(() => {
      return formData.value.textarea.split("\n").length;
    });

    const rowCounter = () => {
      if (rowCounted.value > 2 && rowCounted.value < 18) {
        rowCount.value = rowCounted.value;
      } else if (rowCounted.value >= 18) {
        rowCount.value = 18;
      } else {
        rowCount.value = 2;
      }
    };

    const changeName = (event: any) => {
      console.log("[Event] ", event);
    }

    const textLength = computed(() => formData.value.textarea.length);

    const componentKey = ref(0);

    const routeBack = () => {
      isTrue.value = false;
      componentKey.value++;
      formData.value.firstName = "";
      formData.value.lastName = "";
      formData.value.patronymicName = "";
      formData.value.tel = "";
      formData.value.textarea = "";
    };

    return {
      formData,
      textLength,
      submitForm,
      formatPhoneNumber,
      formIsValid,
      isTrue,
      patternValue,
      rowCount,
      rowCounter,
      rowCounted,
      patternPhone,
      changeName,
      routeBack,
      componentKey,
    };
  },
};
</script>

<style scoped>
#all-right {
  height: 251px;
  width: 305px;
}

#back {
  margin: 10px auto;
  width: 50%;
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
  font-size: 0.96em;
  margin-right: 5px;
}

.star-red {
  color: #ff0000;
}

.field__input {
  min-width: 60%;
  width: 200px;
}

.field__button {
  /* align-self: flex-start; */
  /* top|right|down|left */
  margin-right: 40%;
  padding: 4px 6px;
}

textarea {
  resize: none;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue",
    sans-serif;
  padding: 4px;
  border-radius: 2px;
}
:active,
:hover,
:focus {
  outline: 0;
  outline-offset: 0;
}

.valid {
  margin-right: 0px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  font-size: 0.7em;
}

.box {
  border: 1px solid #979797;
  border-radius: 2px;
  padding: 5px;
  margin-top: 10px;
  text-align: center;
}

.head {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  text-align: center;
}

/* .clone {
  border: 1px solid #000;
  border-radius: 2px;
  margin-right: 0px;
  margin-left: auto;
  width: 200px;
  font-size: 0.9em;
  text-align: left;
} */

@media (max-width: 369px) {
  .field {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .field__button {
    margin: 0;
  }
}
</style>
