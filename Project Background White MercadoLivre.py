from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def verificar_listagem(pagina, initializePage, driver):
    
    try:
        # Inicializa o WebDriver
        if initializePage == True:
            service = Service("C:/Users/Tiall/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
            driver = webdriver.Chrome(service=service)  # Use o caminho do ChromeDriver se necessário
            
        

        # Abre uma página
        driver.get("https://www.mercadolivre.com.br/anuncios/lista?filters=OMNI_INACTIVE&page=" + str(pagina) + "&sort=DEFAULT")

        if driver != None:
            try:
                time.sleep(5)
                aux = driver.find_element(By.CSS_SELECTOR, "div[class='ui-empty-state__container']")

                verificar_listagem(pagina, False, driver)
            except:
                aux = False
        loadPage = False

        time.sleep(5)

        # Achar a lista de itens da grid
        grid = driver.find_element(By.CLASS_NAME, "sc-list-grid__rows")
        # Achar a lista de botoes
        gridProductLines = grid.find_elements(By.CLASS_NAME, "sc-list-item-row--inactive")
        
        index = 0

        while index < len(gridProductLines):
            
            if loadPage == True:
                driver.get("https://www.mercadolivre.com.br/anuncios/lista?filters=OMNI_INACTIVE&page=" + str(pagina) + "&sort=DEFAULT")
                time.sleep(10)
                grid = driver.find_element(By.CLASS_NAME, "sc-list-grid__rows")
                # Achar a lista de botoes
                gridProductLines = grid.find_elements(By.CLASS_NAME, "sc-list-item-row--inactive")

            sectionInactived = gridProductLines[index].find_element(By.CSS_SELECTOR, "div[class='sc-list-dynamic-cell sc-list-cell-separator']")

            textWhyInnactive = sectionInactived.find_element(By.CSS_SELECTOR,"div[class='sc-list-actionable-cell__description sc-list-text--secondary']").find_element(By.TAG_NAME,"p").text

            if "tamanho" not in textWhyInnactive and "marcas" not in textWhyInnactive and "catálogo" not in textWhyInnactive and "outro anunciado" not in textWhyInnactive and "Você" not in textWhyInnactive:

                btnCorrigirFoto = sectionInactived.find_element(By.CLASS_NAME, "sc-list-actionable-cell__action")

                driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", gridProductLines[index], 200)

                time.sleep(1)

                btnCorrigirFoto.click()

                time.sleep(5)

                sectionFotos = None
                try:
                    sectionFotos = driver.find_element(By.ID, "picture_uploader_task")
                except:
                    sectionFotos = driver.find_element(By.ID, "variations_task")

                btnExpandSectionFotos = sectionFotos.find_element(By.TAG_NAME,"button")

                driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", btnExpandSectionFotos, 100)

                time.sleep(1)

                btnExpandSectionFotos.click()

                time.sleep(1)

                # Agora vamos ver se tem Variação Ou se não tem variação

                sectionEditFoto = None
                lstFoto = None
                # Aqui é com variação
                try:
                    try:
                        sectionEditFoto = sectionFotos.find_element(By.CLASS_NAME, "syi-variations-table")
                    except:
                        sectionEditFoto = sectionFotos.find_element(By.CLASS_NAME, "syi-cw-variations-table")
                    
                    btnExpandEditFoto = sectionEditFoto.find_element(By.CSS_SELECTOR, "td[class='andes-table__column andes-table__column--left andes-table__column--vertical-align-center andes-table__expandable andes-table__expandable-close syi-variations-table__cell syi-variations-table__cell--characteristics']")
                    btnExpandEditFoto.click()
                    time.sleep(1)

                #Aqui é sem variação
                except:
                    sectionEditFoto = sectionFotos.find_element(By.CLASS_NAME, "syi-photos")
                #Pega toda a lista li de fotos
                lstFoto = sectionEditFoto.find_elements(By.CLASS_NAME, "andes-file-uploader__sortable-item")
                if len(lstFoto) == 0:
                    sectionEditFoto = sectionFotos.find_element(By.CLASS_NAME, "syi-photos")
                    lstFoto = sectionEditFoto.find_elements(By.CLASS_NAME, "andes-file-uploader__sortable-item")
                indexFoto = 0
                while indexFoto < len(lstFoto):
                    #Caso já tenha passado pela modal tem que recarregar o DOM da lista
                    if(indexFoto != 0):
                        lstFoto = sectionEditFoto.find_elements(By.CLASS_NAME, "andes-file-uploader__sortable-item")
                    btnEditFoto = lstFoto[indexFoto].find_element(By.CSS_SELECTOR, "button[class='syi-photos_edit-photo andes-file-uploader__thumbnail-close']")
                    try:
                        btnEditFoto.click()
                        btnEditFoto.click()
                        time.sleep(1)
                    except:
                        time.sleep(1)

                    modal = driver.find_element(By.CSS_SELECTOR, "div[class='andes-modal photo-studio__main-modal andes-modal--small']")
                    modalSection = modal.find_element(By.CLASS_NAME, "photo-studio__main-modal__tools")
                    checkAjusteAutomatico = modalSection.find_element(By.CLASS_NAME, "andes-switch__input")

                    checkAjusteAutomatico.click()
                    time.sleep(10)

                    btnConfirmarModal = modal.find_element(By.CLASS_NAME, "andes-modal__actions").find_element(By.CSS_SELECTOR, "button[class='andes-button andes-button--large andes-button--loud']")
                    btnConfirmarModal.click()
                    time.sleep(10)

                    indexFoto +=1

                btnSaveFoto = sectionFotos.find_element(By.CSS_SELECTOR,"button[class='andes-button andes-button--large andes-button--loud']")

                driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", btnSaveFoto, 100)

                btnSaveFoto.click()
                time.sleep(5)

                loadPage = True

            else:
                index += 1

        pagina+= 1  

    except:
        if(pagina<70):
            verificar_listagem(pagina, False, driver)
                      
    finally:
        if(pagina<70):
            verificar_listagem(pagina, False, driver)
        # Fecha o navegador
        # driver.quit()




# Executa a função
if __name__ == "__main__":
    verificar_listagem(1, True, None)