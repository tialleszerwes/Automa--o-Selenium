from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def verificar_listagem(pagina, initializePage, driver):
    
    try:
        produtoJaAtualizado = False
        # Inicializa o WebDriver
        if initializePage == True:
            service = Service("C:/Users/Tiall/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
            driver = webdriver.Chrome(service=service)  # Use o caminho do ChromeDriver se necessário
            

        # Abre uma página
        driver.get("https://seller.magalu.com/products?has_next=true&page=" + str(pagina) + "&per_page=100")
        waitLoadPage = False
        time.sleep(25)

        # Achar a lista de itens da grid
        grid = driver.find_element(By.XPATH, "//div[@class='MaasProduct-MuiGrid-root MaasProduct-MuiGrid-item MaasProduct-MuiGrid-zeroMinWidth MaasProduct-MuiGrid-grid-md-12']")
        # Achar a lista de botoes
        gridProductLines = grid.find_elements(By.XPATH, "//div[contains(@class, 'MaasProduct-MuiPaper-root') and contains(@class, 'sc-jMakVo') and contains(@class, 'sc-iMTnTL') and contains(@class, 'juGMff')]")
        
        
        index = 0

        while index < len(gridProductLines):
            
            if waitLoadPage == True:
                driver.get("https://seller.magalu.com/products?has_next=true&page=" + str(pagina) + "&per_page=100")
                time.sleep(25)
                grid = driver.find_element(By.XPATH, "//div[@class='MaasProduct-MuiGrid-root MaasProduct-MuiGrid-item MaasProduct-MuiGrid-zeroMinWidth MaasProduct-MuiGrid-grid-md-12']")
                # Achar a lista de botoes
                gridProductLines = grid.find_elements(By.XPATH, "//div[contains(@class, 'MaasProduct-MuiPaper-root') and contains(@class, 'sc-jMakVo') and contains(@class, 'sc-iMTnTL') and contains(@class, 'juGMff')]")
        

            # Aqui tem o botão para acessar o produto
            productFirsLine = gridProductLines[index].find_element(By.CSS_SELECTOR, "div.sc-jGKxIK.dDvDqC")
            # Aqui tem a pontuação e status do Produto
            productSecondLine = gridProductLines[index].find_element(By.CSS_SELECTOR, "div.sc-fTFjTM.dNzdMj")

            txtPontos = productSecondLine.find_element(By.TAG_NAME, "text").text

            txtStatusProduto =  productFirsLine.find_element(By.CSS_SELECTOR, "span.MaasProduct-MuiPill-label").text

            if txtStatusProduto == "Bloqueado" and int(txtPontos) < 70:
                # buttonEdit = productFirsLine.find_element(By.CSS_SELECTOR, "button.MaasProduct-MuiButtonBase-root.MaasProduct-MuiIconButton-root.MaasProduct-MuiIconButton-colorSecondary.MaasProduct-MuiIconButton-sizeSmall[title='Editar']")
                waitLoadPage = True
                # Mantem o foco da tela no produto que está sendo editado, com uma margem de 2 produtos por causa do Float Header
                if index > 2:
                    driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", gridProductLines[index], 200)

                buttonEdit = WebDriverWait(productFirsLine, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MaasProduct-MuiButtonBase-root.MaasProduct-MuiIconButton-root.MaasProduct-MuiIconButton-colorSecondary.MaasProduct-MuiIconButton-sizeSmall[title='Editar']"))
                )
            
                buttonEdit.click()
                # inProgressEdit = True

                time.sleep(10)

                divLstSection = driver.find_element(By.TAG_NAME, "form").find_element(By.CLASS_NAME, "pb-11").find_elements(By.XPATH, "./div")

                # Descreva Seu Produto - TITULO, MARCA E DESCRIÇÃO COMPLETA
                div1 = divLstSection[1]

                lstInputs = div1.find_elements(By.TAG_NAME, "input")
    	        # Marca
                
                if "Outras" in lstInputs[3].get_attribute("value"):
                     
                    driver.execute_script("arguments[0].value = 'Az Peças';", lstInputs[3])

                divDescricaoCompleta = div1.find_element(By.CSS_SELECTOR, "div.ql-editor")

                driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", divDescricaoCompleta, 200)

                # Campo Descrição Completa
                if len(divDescricaoCompleta.get_attribute("outerHTML")) < 500:
                     
                    driver.execute_script("arguments[0].innerHTML = '';", divDescricaoCompleta)

                    txtDescricao = "<p>" + lstInputs[0].get_attribute("value") + "</p>"
                    txtDescricao += (
                        "<p>Produto Novo, com NOTA FISCAL e Garantia 90 dias</p>"
                        "<p>---------------------------------------------------</p>"
                        "<p> ATENÇÃO </p>"
                        "<p>---------------------------------------------------</p>"
                        "<p>Confira o seu endereço de entrega cadastrado, não alteramos endereços após a compra.</p>"
                        "<p>---------------------------------------------------</p>"
                        "<p>HORÁRIO DE ATENDIMENTO</p>"
                        "<p>---------------------------------------------------</p>"
                        "<p>Segunda à Sexta das 08h00 às 18h00</p>"
                        "<p>Sábado das 08h00 às 13h00</p>"
                        "<p>---------------------------------------------------</p>"
                        "<p>DÚVIDAS FREQUENTES:</p>"
                        "<p>---------------------------------------------------</p>"
                        "<p>1 - COMO VERIFICAR SE O PRODUTO É COMPATÍVEL COM O MEU APARELHO?</p>"
                        "<p>R: Geralmente o modelo fica localizado na etiqueta colada atrás, embaixo ou dentro (lateral) do aparelho, depois é só confirmar se o modelo confere com a descrição do anúncio. Verifique se as informações do produto conferem com as descrições listadas acima. Lembrando se seu modelo é atual pode ser que a lista esteja desatualizada, confirme no campo de perguntas conosco.</p>"
                        "<p>2 - O CÓDIGO DA PEÇA É O MESMO, MAS NÃO ENCONTREI MEU MODELO NA DESCRIÇÃO, O QUE EU FAÇO?</p>"
                        "<p>R: Modelos novos podem não constar na descrição. Mas o código de identificação da peça é a parte mais relevante, então se ela corresponde ao que você busca pode efetuar a compra.</p>"
                        "<p>3 - O MODELO DO MEU APARELHO É O MESMO, MAS O CÓDIGO DA PEÇA NÃO CONFERE, O QUE EU FAÇO?</p>"
                        "<p>R: O código do fornecedor (peça) é um código que ao decorrer do tempo é atualizado pelo fabricante. Para termos certeza, nos envie ele que confirmamos para você se está tudo certo antes de efetuar a compra.</p>"
                        "<p>4 - QUANTO TEMPO TENHO PARA DEVOLVER? E COMO FAÇO?</p>"
                        "<p>R: De acordo com o Código De Defesa Do Consumidor, você tem 7 dias para gerar uma devolução sem custos adicionais.</p>"
                        "<p>R: Para realizar a devolução, acesse sua conta, clique em detalhes do pedido e após na opção \"Devolver\" ou \"Central De Atendimento\".</p>"
                        "<p>5 - COMO CALCULAR O VALOR DO FRETE?</p>"
                        "<p>R: Informe seu CEP no campo que fica abaixo ou acima do botão comprar para pesquisa do endereço; a plataforma apresentará opções disponíveis para a sua região.</p>"
                        "<p>Utilize o campo de perguntas e somente clique em comprar após ter plena certeza.</p>"
                    )

                    driver.execute_script("arguments[0].innerHTML = '" + txtDescricao +"';", divDescricaoCompleta)
                

                # >>>>>>>>DIV3<<<<<<<<<<<

                section3 = divLstSection[3]

                driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", section3, 200)
                

                checkboxes = section3.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

                if checkboxes[0].is_selected() == False:
                    checkboxes[0].click()
                if checkboxes[1].is_selected() == False:
                    checkboxes[1].click()



                # >>>>>>>>>>>DIV5<<<<<<<<<<

                section5 = divLstSection[5]

                driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", section5, 200)


                lstInputsDiv5 = section5.find_elements(By.TAG_NAME, "input")
                
                # lstInputsDiv5[0].clear()
                # lstInputsDiv5[1].clear()
                # lstInputsDiv5[2].clear()
                # lstInputsDiv5[3].clear()
                # lstInputsDiv5[5].clear()
                # lstInputsDiv5[4].clear()
                
                if lstInputsDiv5[0].get_attribute("value") == "" or lstInputsDiv5[1].get_attribute("value") == "":
                    lstInputsDiv5[0].send_keys("Garantia")
                    lstInputsDiv5[1].send_keys("3 Meses")

                if lstInputsDiv5[2].get_attribute("value") == "" or lstInputsDiv5[3].get_attribute("value") == "":
                    lstInputsDiv5[2].send_keys("Fornecedor")
                    lstInputsDiv5[3].send_keys(lstInputs[3].get_attribute("value"))

                if lstInputsDiv5[4].get_attribute("value") == "" or lstInputsDiv5[5].get_attribute("value") == "":
                    lstInputsDiv5[4].send_keys("Tipo De Garantia")
                    lstInputsDiv5[5].send_keys("Loja")
                else:
                    produtoJaAtualizado = True

                # >>>>>>>DIV9<<<<<

                section9 = divLstSection[9]

                sectionImage = None
                # Verifica se tem variação
                try:
                    buttonOpenImage = section9.find_element(By.CSS_SELECTOR, "button.MaasProduct-MuiButtonBase-root.MaasProduct-MuiButton-root.MaasProduct-MuiButton-text")
                    
                    driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", section9, 200)


                    time.sleep(1)

                    buttonOpenImage.click()

                    time.sleep(2)

                    modal = driver.find_element(By.CSS_SELECTOR, "div[role='presentation'].MaasProduct-MuiDialog-root")

                    sectionImage = modal
                # Caso não tenha variação
                except:
                    
                    section4 = divLstSection[4]
                    
                    driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - arguments[1]);", section4, 200)
                    
                    time.sleep(1)

                    sectionImage = section4

                input_file = sectionImage.find_element(By.CSS_SELECTOR, "input[type='file'][accept='image/jpeg,image/png,image/webp'][multiple]")

                caminho_imagem1 = None
                if len(sectionImage.find_elements(By.TAG_NAME, "img")) < 2:
                    input_file = sectionImage.find_element(By.CSS_SELECTOR, "input[type='file'][accept='image/jpeg,image/png,image/webp'][multiple]")
                    caminho_imagem1 = 'C:/Users/Tiall/OneDrive/Área de Trabalho/Design sem nome.jpg'


                if produtoJaAtualizado == False:
                    input_file = sectionImage.find_element(By.CSS_SELECTOR, "input[type='file'][accept='image/jpeg,image/png,image/webp'][multiple]")
                    caminho_imagem = 'C:/Users/Tiall/OneDrive/Área de Trabalho/Design sem nome (1).jpg'
                    if caminho_imagem1 != None:
                        input_file.send_keys(f'{caminho_imagem}\n{caminho_imagem1}')
                    else:
                        input_file.send_keys(caminho_imagem)
                    # Realiza operações adicionais na nova página se necessário
                    time.sleep(5)  
                else:
                    if len(sectionImage.find_elements(By.TAG_NAME, "img")) <= 2:
                        input_file = sectionImage.find_element(By.CSS_SELECTOR, "input[type='file'][accept='image/jpeg,image/png,image/webp'][multiple]")
                        caminho_imagem = 'C:/Users/Tiall/OneDrive/Área de Trabalho/Design sem nome.jpg'
                        time.sleep(1)
                        input_file.send_keys(caminho_imagem)
                        time.sleep(4)

                try:
                    btnConfirmarSelecao = modal.find_element(By.CSS_SELECTOR, "button.MaasProduct-MuiButton-contained.MaasProduct-MuiButton-containedPrimary > .MaasProduct-MuiButton-label")
                    btnConfirmarSelecao.click()

                    time.sleep(2)  
                except:
                    time.sleep(1) 
                divRodape = driver.find_element(By.CSS_SELECTOR, "div.MaasProduct-MuiPaper-root.MaasProduct-MuiPaper-elevation8.MaasProduct-MuiPaper-rounded")

                buttonSubmitProduto = divRodape.find_element(By.CSS_SELECTOR, "button[type='submit'].MaasProduct-MuiButton-containedSuccess[aria-label='Enviar para atualização']")

                buttonSubmitProduto.click()

            else:
                waitLoadPage = False

            index += 1
        pagina+= 1
        if(pagina<70):
            verificar_listagem(pagina, False, driver)      

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
    verificar_listagem(10, True, None)