/**
 * Класс Одиночка определяет геттер `instance`, который позволяет клиентам
 * получить доступ к уникальному экземпляру одиночки.
 */
class Singleton {
  static #instance: Singleton;

  /**
   * Конструктор Одиночки всегда должен быть скрытым, чтобы предотвратить
   * создание объекта через оператор new.
   */
  private constructor() {}

  /**
   * Статический геттер, управляющий доступом к экземпляру одиночки.
   *
   * Эта реализация позволяет вам расширять класс Одиночки, сохраняя повсюду
   * только один экземпляр каждого подкласса.
   */
  public static get instance(): Singleton {
    if (!Singleton.#instance) {
      Singleton.#instance = new Singleton();
    }

    return Singleton.#instance;
  }

  /**
   * Наконец, любой одиночка может содержать некоторую бизнес-логику, которая
   * может быть выполнена на его экземпляре.
   */
  public someBusinessLogic() {
    // ...
  }
}

/**
 * Клиентский код.
 */
function clientCode() {
  const s1 = Singleton.instance;
  const s2 = Singleton.instance;

  if (s1 === s2) {
    console.log("Singleton works, both variables contain the same instance.");
  } else {
    console.log("Singleton failed, variables contain different instances.");
  }
}

clientCode();
