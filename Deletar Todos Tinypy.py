from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verificar_listagem():
    
    try:
        # Inicializa o WebDriver
        driver = webdriver.Chrome()  # Use o caminho do ChromeDriver se necessário
        # Abre uma página
        driver.get("https://erp.tiny.com.br/anuncios?idEcommerce=15625#list")


        while True:
            time.sleep(8)
            # Achar a lista de itens da grid
            btnCheckAll = driver.find_element(By.CSS_SELECTOR, 'th.checkbox-datatable input[type="checkbox"]')
            # Força o clique
            driver.execute_script("arguments[0].click();", btnCheckAll)

            # driver.execute_script("toggleCheck(\"#tabelaListagem\")")

            btnMaisAcoes = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-menu-acoes.dropdown-toggle[data-toggle='dropdown']")

            # btnMaisAcoes = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-menu-acoes.dropdown-toggle[data-toggle='dropdown']"))
            # )
            driver.execute_script("arguments[0].click();", btnMaisAcoes)
            # btnMaisAcoes.click()

            btnExluirTudo = driver.find_element(By.CSS_SELECTOR, "a[href='#'][onclick='anuncios.excluirSelecionados(); return false;']")

            # btnExluirTudo = WebDriverWait(btnExluirTudo, 10).until(
            #     EC.element_to_be_clickable((By.TAG_NAME, 'a'))
            # )

            driver.execute_script("arguments[0].click();", btnExluirTudo)

            # btnConfirmaExclusao = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-sm.btn-primary[popup-action='confirm'][popup-action-id='0']")

            btnConfirmaExclusao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-sm.btn-primary[popup-action='confirm'][popup-action-id='0']"))
            )

            btnConfirmaExclusao.click()
        

    except:
        verificar_listagem()
                      
    finally:

       driver.close()




# Executa a função
if __name__ == "__main__":
    verificar_listagem()