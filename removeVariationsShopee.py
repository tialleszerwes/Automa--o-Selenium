from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter


def verificar_listagem(login, driver, pagina):
    
    secondTabOpen = False
    try:
       
        if login == False: 

             # Inicializa o WebDriver
            driver = webdriver.Chrome()  # Use o caminho do ChromeDriver se necessário
            actions = ActionChains(driver)
            # Abre uma página
            driver.get("https://seller.shopee.com.br/portal/product/list/all?page=" + str(pagina) + "&size=12")

            driver.execute_script("document.body.style.zoom='40%'")

            time.sleep(10)
            inputLogin = driver.find_element(By.CSS_SELECTOR, "[name='loginKey']")

            inputLogin.clear()
            inputLogin.send_keys("marketplace@assistecpoa.com.br")
        
            inputPassword = driver.find_element(By.CSS_SELECTOR, "[name='password']")

            inputPassword.clear()
            inputPassword.send_keys("Sh$#@ssis20@bill")

            submitButton = driver.find_elements(By.CLASS_NAME, "Q4KP5g")
        
            actions.move_to_element(submitButton[1]).click().perform()

            time.sleep(3)

            actions.move_to_element(submitButton[0]).click().perform()

            time.sleep(20)

        else :
                pagina += 1
                driver.get("https://seller.shopee.com.br/portal/product/list/all?page=" + str(pagina) + "&size=12")
                time.sleep(4)
        

        

        # BtnModal = driver.find_element(By.XPATH, '//button[@type="button" and contains(@class, "eds-button") and contains(@class, "eds-button--primary") and contains(@class, "eds-button--normal")]')

        # time.sleep(3)

        # actions.move_to_element(BtnModal).click().perform()

        # time.sleep(3)

        # Achar a lista de itens da grid
        grid = driver.find_elements(By.CLASS_NAME, "eds-table__body-container")[0]
        # Achar a lista de botoes
        gridBody = grid.find_element(By.CLASS_NAME, "eds-table__fix-body")

        gridTable = gridBody.find_element(By.TAG_NAME, "table")

        linesTrCount = gridTable.find_elements(By.TAG_NAME,"tr")
        
        # buttons = gridButtons.find_element(By.)
        index = 0
        # for item in linesTr:
        # while index < 1:
        while index < len(linesTrCount):
            
             # Achar a lista de itens da grid
            grid = driver.find_elements(By.CLASS_NAME, "eds-table__body-container")[0]
            # Achar a lista de botoes
            gridBody = grid.find_element(By.CLASS_NAME, "eds-table__fix-body")

            gridTable = gridBody.find_element(By.TAG_NAME, "table")

            linesTr = gridTable.find_elements(By.TAG_NAME,"tr")

            # buttonEdit = item.find_element(By.TAG_NAME,"button")
            if index > 2:
                driver.execute_script("arguments[0].scrollIntoView();", linesTr[index-2])

            buttonEdit = WebDriverWait(linesTr[index], 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, 'button'))
            )
            
            # VERIFICA SE TEM VARIAÇÃO 
            gridBodyVariacao = grid.find_element(By.CLASS_NAME, "eds-table__main-body")
            gridLinhasVariacao = gridBodyVariacao.find_elements(By.CLASS_NAME, "eds-table__row")
            temVariacao = True
            try:
                  gridFilhoLinhasVariacao = gridLinhasVariacao[index].find_elements(By.CLASS_NAME, "view-more")
                  if len(gridFilhoLinhasVariacao) < 1:
                       temVariacao = False
            except:
                temVariacao = False
            # Verifica se o item possui o elemento específico
            # elemento_especifico = item.find_elements(By.CLASS_NAME, "view-more padding-bottom")
            if temVariacao:
                # Acessa o item (pode ser um link, botão, etc.)
                # link = item.find_element(By.TAG_NAME, "a")  # Exemplo de acessar um link
                # link.click()

                buttonEdit.click()
                secondTabOpen = True
                # actions.move_to_element(buttonEdit).click().perform()
                # button.click()
                # TODO COLOCAR UM VALIDADOR DE TEMPO DESCENTE
                time.sleep(5)
                # Troca para a nova aba
                driver.switch_to.window(driver.window_handles[-1])
                # Action nova aba
                actions = ActionChains(driver)

                divSection = driver.find_element(By.CSS_SELECTOR,'div[class="product-detail-panel product-sales-info"]')

                divPrice = divSection.find_element(By.CLASS_NAME, "product-edit-input")

                inputPrice = divPrice.find_element(By.CSS_SELECTOR, "input[data-v-0ea4e9de]")

                price = inputPrice.get_attribute("value")

                divStock = driver.find_elements(By.CLASS_NAME, "stock-column")

                inputStock = divStock[1].find_element(By.CSS_SELECTOR, "input[data-v-0ea4e9de]")

                stock = inputStock.get_attribute("value")

                divInfoVenda = driver.find_element(By.CLASS_NAME, "product-sales-info")

                lstSpanX = divInfoVenda.find_elements(By.CLASS_NAME,"variation-delete-btn")
                
                span_element = None
                pulaProfuto = False
                try:
                    # span_element = driver.find_element(By.XPATH, '//span[@class="item-title-text" and text()="País de Origem"]')
                     span_element = driver.find_element(By.CSS_SELECTOR, "button.primary-link-button.shopee-button.shopee-button--link.shopee-button--normal")
                except:
                    span_element = driver.find_element(By.XPATH, "//div[text()='Especificação']")


                if pulaProfuto == False:
                    driver.execute_script("arguments[0].scrollIntoView();", span_element)

                    time.sleep(2)

                    lstSpanX[0].click()

                    # actions.move_to_element(lstSpanX[0]).click().perform()

                    time.sleep(1)

                    lstSpanX = divInfoVenda.find_elements(By.CLASS_NAME,"variation-delete-btn")

                    time.sleep(1)

                    lstSpanX[0].click()

                    # actions.move_to_element(lstSpanX[0]).click().perform()

                    # Pega o DOM da nova aba
                    # dom_nova_aba = driver.page_source

                    time.sleep(1)

                    # Depois de ter excluido busca de novo a section
                    divInfoVenda = driver.find_element(By.CLASS_NAME, "product-sales-info")

                    lstInputs = divInfoVenda.find_elements(By.TAG_NAME, "input")

                    # Preço
                    lstInputs[0].clear()
                    lstInputs[0].send_keys(price)

                    # estoque
                    lstInputs[1].clear()
                    lstInputs[1].send_keys(stock)

                    time.sleep(1)

                    # Seleciona o input usando XPath
                    inputTitle = driver.find_element(By.XPATH, '//input[@type="text" and @placeholder="Nome da Marca + Tipo do Produto + atributos chave (Materiais, Cores, Tamanho e Modelo)"]')
                    txtTile = inputTitle.get_attribute("value")
                    txtTile = txtTile.strip()
                    inputTitle.clear()
                    inputTitle.send_keys(txtTile)

                    time.sleep(1)

                    # Trocar Preço devido a erro de campo não preenchido
                    divInfoShipping = driver.find_element(By.CLASS_NAME, "product-shipping")
                    lstInputs = divInfoShipping.find_elements(By.TAG_NAME, "input")
                    inputWeight = lstInputs[0]
                    txtWeight = inputWeight.get_attribute("value")
                    floatWeight = float(txtWeight)
                    floatWeight += 0.01
                    floatWeight = round(floatWeight,2)
                    txtWeight = str(floatWeight)
                    inputWeight.clear()
                    inputWeight.send_keys(txtWeight)


                    time.sleep(1)

                    # btnSave = driver.find_element(By.XPATH, '//button[@type="button" and contains(@class, "eds-button--xl-large") and contains(@class, "eds-button--primary") and contains(@class, "eds-button--normal")]/span[text()=" Atualizar "]')

                    # driver.execute_script("arguments[0].scrollIntoView();", btnSave)


                    btnSave = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()=' Atualizar ']]"))  # Substitua pelo seu seletor
                    )

                    btnSave.click()

                    time.sleep(1)

                    botao_atualizar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Atualizar']]"))  # Substitua pelo seu seletor
                    )


                    # Botão Modal
                    botao_atualizar.click()

                    time.sleep(3)

                # Fecha a aba atual
                driver.close()

                
                # Realiza operações adicionais na nova página se necessário
                time.sleep(2)  # Aguardar o carregamento da nova página
                # driver.back()  # Volta para a página de listagem

                # Volta para a aba original
                driver.switch_to.window(driver.window_handles[0])

                # Re-localiza os itens, pois a navegação pode alterá-los
                # itens = driver.find_elements(By.CSS_SELECTOR, "SELETOR_DOS_ITENS")
            index += 1

        verificar_listagem(True, driver,pagina)      

    except:
         if secondTabOpen == True:
              # Fecha a aba atual
                driver.close()
                # Volta para a aba original
                driver.switch_to.window(driver.window_handles[0])
                # Para manter a pagina atual -1
         verificar_listagem(True, driver,pagina-1)
                      
    finally:

        if secondTabOpen == True:
              # Fecha a aba atual
                driver.close()
                # Volta para a aba original
                driver.switch_to.window(driver.window_handles[0])
                # Para manter a pagina atual -1

        verificar_listagem(True, driver,pagina-1)
        # Fecha o navegador
        # driver.quit()




# Executa a função
if __name__ == "__main__":
    verificar_listagem(False, None, 1)