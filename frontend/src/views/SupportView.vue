<script setup lang="ts">
import FormInput from "../components/FormInput.vue";
</script>

<template>
  <div class="about">
    <div>
      <h2>Заполните поля формы ниже</h2>
    </div>
    <div>
      <FormInput />
    </div>
  </div>
</template>

<style>
div .about {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
}
</style>
